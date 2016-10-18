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
from tickets.model import CommentModel, TicketModel
from imgserv.model import ImageModel
from users.model import UserModel, TokenModel
from common.cryptography import Cryptography


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
            "url": self.__image_base_url + Cryptography.encryptAES_CFB((prefix + str(object_id)).encode())
        }

    def createTicket(self, request, dto):
        """

        :param request:
        :param dto:
        :return:
        """

        try:
            # find the user
            ticket = self.dbConn.get_connection(TokenModel).find_one({"token": dto.access_token})

            if not ticket:
                return BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST

            userDict = self.dbConn.get_connection(UserModel).find_one({"_id": ticket["user_id"]})
            user = UserModel.fromDict(userDict)

            if not user:
                return BaseError.USER_NOT_FOUND, status.HTTP_400_BAD_REQUEST

            # decode the images
            images = list()
            image_ids = list()
            ticket_id = ObjectId()
            commentId = ObjectId()
            for imageData in dto.images:
                image = base64.b64decode(imageData)
                mime_type = magic.from_buffer(image, mime=True)
                if "image" not in mime_type or\
                        ("png" not in mime_type and "jpg" not in mime_type and "jpeg" not in mime_type):
                    return BaseError.FILE_TYPE_NOT_SUPPORTED, status.HTTP_400_BAD_REQUEST

                try:
                    with Image(blob=image) as img:
                        if img.height is None or img.width is None:
                            return BaseError.INVALID_IMAGE, status.HTTP_400_BAD_REQUEST

                        _id = ObjectId()
                        self.__writeImage(image, _id)
                        thumbnail = self.__imageResize(_id, img, roadro_limits.THUMBNAIL_SIZE)

                        imgModel = ImageModel()
                        imgModel.url = self.__image_base_url + Cryptography.encryptAES_CFB(str(_id).encode())
                        imgModel.width = img.width
                        imgModel.height = img.height
                        imgModel.metadata = thumbnail
                        imgModel.ticket_id = ticket_id
                        imgModel.mimetype = mime_type
                        imgModel.user_id = user.id
                        imgModel.id = _id

                        image_ids.append(_id)
                        images.append(imgModel.toDict())

                except Exception as e:
                    logger.error(stackTrace(e))
                    return BaseError.INTERNAL_SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR

            for image in images:
                self.dbConn.get_connection(ImageModel).insert_one(image)

            commentModel = None
            if dto.comment:
                commentModel = CommentModel()
                commentModel.id = commentId
                commentModel.user_id = user.id
                commentModel.text = dto.comment
                commentModel.ticket_id = ticket_id
                commentModel.created_date = datetime.datetime.utcnow()
                self.dbConn.get_connection(CommentModel).insert(commentModel.toDict())

            ticketModel = TicketModel()
            ticketModel.user_id = user.id
            ticketModel.id = ticket_id
            ticketModel.image_ids = image_ids
            ticketModel.comment_ids = [commentId] if dto.comment else []
            ticketModel.address = dto.address
            ticketModel.latitude = dto.lat
            ticketModel.longitude = dto.long
            ticketModel.resolution = TicketModel.UNASIGNED
            ticketModel.created_date = datetime.datetime.utcnow()

            self.dbConn.get_connection(TicketModel).insert(ticketModel.toDict())

            resp = dict(response=dict())

            hostname = ("https://" if request.is_secure() else "http://") + request.get_host()

            resp["response"] = {
                "id": Cryptography.encryptAES_CFB(str(ticket_id).encode()),
                "images": [
                    {
                        "orig_url": hostname + image["url"],
                        "thumb": {
                            "url": hostname + image["metadata"]["url"],
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

    def getMyTickets(self, request, dto):
        """

        :param request:
        :param dto:
        :return:
        """

        try:

            tokenModel = self.dbConn.get_connection(TokenModel).find_one({"token": dto.access_token})
            if not tokenModel:
                return BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST



            return {"error": {"code": 1000, "message": "Not implemented yet"}}, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            logger.error(stackTrace(e))
            return BaseError.INTERNAL_SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR
