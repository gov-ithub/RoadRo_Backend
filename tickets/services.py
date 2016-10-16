# coding=utf-8
import base64
import magic
import os
import logging
import datetime
from common.base_service import BaseService
from common.roadro_errors import BaseError
from common import http_status as status
from common import roadro_limits
from common import roadro_constants
from common.utils import stackTrace
from wand.image import Image
from bson.objectid import ObjectId
from tickets.model import ImageModel, CommentModel, TicketModel
from users.model import UserModel


logger = logging.getLogger(__name__)


class TicketService(BaseService):
    """
    services for tickets
    """

    def __init__(self, dbConnection, image_base_url, storage_path):
        """

        :param dbConnection:
        """
        super(TicketService, self).__init__(dbConnection)
        self.__image_base_url = image_base_url
        self.base_img_path = storage_path

    def __writeImage(self, binary_buffer, object_id):
        """

        :param binary_buffer:
        :param object_id:
        :return:
        """
        path1 = self.base_img_path + str(object_id)[-2:]
        path2 = os.path.join(path1, str(object_id)[-4:-2])
        if not os.path.exists(path1):
            os.mkdir(path1)
        if not os.path.exists(path2):
            os.mkdir(path2)

        new_output = os.path.join(path2, str(object_id))
        with open(new_output, "wb") as f:
            f.write(binary_buffer)

    def __imageResize(self, object_id, img, max_size=roadro_limits.THUMBNAIL_SIZE):
        """

        :param object_id:
        :param img:
        :param max_size:
        :return:
        """

        # compute which dimension is greater and keep the aspect ratio
        resize = True
        if img.height >= img.width and img.height > max_size:
            newHeight = max_size
            newWidth = int(max_size * img.width / img.height)
        elif img.width > img.height and img.width > max_size:
            newWidth = max_size
            newHeight = int(max_size * img.height / img.width)
        else:
            resize = False
            newHeight = img.height
            newWidth = img.width

        if resize:
            img.resize(width=newWidth, height=newHeight, filter="lanczos")

        path1 = self.base_img_path + str(object_id)[-2:]
        path2 = os.path.join(path1, str(object_id)[-4:-2])
        if not os.path.exists(path1):
            os.mkdir(path1)
        if not os.path.exists(path2):
            os.mkdir(path2)

        prefix = ""
        if max_size == roadro_limits.THUMBNAIL_SIZE:
            prefix = roadro_constants.THUMBNAIL_PREFIX
        newOutput = os.path.join(path2, prefix + str(object_id))

        with open(newOutput, "wb") as f:
            img.save(file=f)

        return {
            "width": newWidth,
            "height": newHeight,
            "url": self.__image_base_url + prefix+ str(object_id)
        }

    def createTicket(self, request, data):
        """

        :param request:
        :param data:
        :return:
        """

        if "access_token" not in data or type(data["access_token"]) is not str or not data["access_token"].strip():
            return BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST

        if "images" not in data:
            return BaseError.MISSING_IMAGES_FIELD, status.HTTP_400_BAD_REQUEST

        if not data["images"] or type(data["images"]) is not list:
            return BaseError.INVALID_IMAGES_FIELD, status.HTTP_400_BAD_REQUEST

        for image in data["images"]:
            if type(image) is not str:
                return BaseError.INVALID_IMAGE_STRING, status.HTTP_400_BAD_REQUEST

        if len(data["images"]) > roadro_limits.MAX_UPLOADED_IMAGES:
            return BaseError.TOO_MANY_IMAGES, status.HTTP_400_BAD_REQUEST

        if "address" not in data or type(data["address"]) is not str or not data["address"].strip():
            return BaseError.INVALID_ADDRESS_FIELD, status.HTTP_400_BAD_REQUEST

        if "lat" in data and type(data["lat"]) not in (float, str, int):
            return BaseError.INVALID_LATITUDE_FIELD, status.HTTP_400_BAD_REQUEST

        if "long" in data and type(data["long"]) not in (float, str, int):
            return BaseError.INVALID_LONGITUDE_FIELD, status.HTTP_400_BAD_REQUEST

        try:
            data["long"] = float(data["long"])
            data["lat"] = float(data["lat"])
        except Exception as e:
            logger.error(stackTrace(e))
            return BaseError.INVALID_LATITUDE_FIELD, status.HTTP_400_BAD_REQUEST

        if "comment" in data and type(data["comment"]) is not str and not data["comment"].strip():
            return BaseError.INVALID_COMMENT_FIELD, status.HTTP_400_BAD_REQUEST

        try:
            # find the user
            ticket = self.dbConn.get_connection("tokens").find_one({"token": data["access_token"]})

            if not ticket:
                return BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST

            userDict = self.dbConn.get_connection("users").find_one({"_id": ticket["user_id"]})
            user = UserModel.fromDict(userDict)

            if not user:
                return BaseError.USER_NOT_FOUND, status.HTTP_400_BAD_REQUEST

            #decode the images
            images = list()
            image_ids = list()
            ticket_id = ObjectId()
            commentId = ObjectId()
            for imageData in data["images"]:
                image = base64.b64decode(imageData)
                mime_type = magic.from_buffer(image, mime=True)
                if "image" not in mime_type:
                    return BaseError.FILE_TYPE_NOT_SUPPORTED, status.HTTP_400_BAD_REQUEST

                try:
                    with Image(blob=image) as img:
                        if img.height is None or img.width is None:
                            return BaseError.INVALID_IMAGE, status.HTTP_400_BAD_REQUEST

                        _id = ObjectId()
                        self.__writeImage(image, _id)
                        thumbnail = self.__imageResize(_id, img, roadro_limits.THUMBNAIL_SIZE)

                        imgModel = ImageModel()
                        imgModel.url = self.__image_base_url + str(_id)
                        imgModel.width = img.width
                        imgModel.height = img.height
                        imgModel.metadata = thumbnail
                        imgModel.ticket_id = ticket_id
                        imgModel.mimetype = mime_type
                        imgModel.id = _id

                        image_ids.append(_id)
                        images.append(imgModel.toDict())

                except Exception as e:
                    logger.error(stackTrace(e))
                    return BaseError.INTERNAL_SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR

            for image in images:
                self.dbConn.get_connection("images").insert_one(image)

            commentModel = None
            if data["comment"]:
                commentModel = CommentModel()
                commentModel.id = commentId
                commentModel.user_id = user.id
                commentModel.text = data["comment"]
                commentModel.ticket_id = ticket_id
                commentModel.created_date = datetime.datetime.utcnow()
                self.dbConn.get_connection("comments").insert(commentModel.toDict())

            ticketModel = TicketModel()
            ticketModel.user_id = user.id
            ticketModel.id = ticket_id
            ticketModel.image_ids = image_ids
            ticketModel.comment_ids = [commentId] if data["comment"] else []
            ticketModel.address = data["address"]
            ticketModel.latitude = data.get("lat")
            ticketModel.longitude = data.get("longitude")
            ticketModel.resolution = TicketModel.UNASIGNED
            ticketModel.created_date = datetime.datetime.utcnow()

            self.dbConn.get_connection("tickets").insert(ticketModel.toDict())

            resp = dict(response=dict())

            resp["response"] = {
                "id": str(ticket_id),
                "images": [
                    {
                        "orig_url": image["url"],
                        "thumb": {
                            "url": image["metadata"]["url"],
                            "width": image["metadata"]["width"],
                            "height": image["metadata"]["height"]
                        }
                    } for image in images],
                "address": ticketModel.address,
                "lat": ticketModel.latitude,
                "long": ticketModel.longitude,
                "comment": commentModel.text if commentModel else None,
                "likes": 0
            }

            return resp, status.HTTP_200_OK
        except Exception as e:
            logger.error(stackTrace(e))
            return BaseError.INTERNAL_SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR


    def getTicket(self, request, data):
        """

        :param request:
        :param data:
        :return:
        """

        return {"error": {"code": 1000, "message": "Not implemented yet"}}, status.HTTP_400_BAD_REQUEST

    def getMyTickets(self, request, data):
        """

        :param request:
        :param data:
        :return:
        """

        return {"error": {"code": 1000, "message": "Not implemented yet"}}, status.HTTP_400_BAD_REQUEST
