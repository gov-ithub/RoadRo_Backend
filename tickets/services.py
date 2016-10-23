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
from tickets.model import CommentModel, TicketModel, LikeModel
from imgserv.model import ImageModel
from common.cryptography import Cryptography
from tickets.serializers import TicketResponseDTO


logger = logging.getLogger(__name__)


class TicketService(BaseService):
    """
    services for tickets
    """

    def __init__(self, daoRegistry, image_base_url, storage_path):
        """

        :param daoRegistry:
        :param image_base_url:
        :param storage_path:
        """
        super(TicketService, self).__init__(daoRegistry)
        self.__image_base_url = image_base_url
        self.base_img_path = storage_path
        self.MAX_FETCHED_TICKETS_COUNT = 30
        self.MAX_FETCHED_COMMENTS_COUNT = 10

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
            "url": self.__image_base_url + Cryptography.simpleEncryption((prefix + str(object_id)).encode())
        }

    def createTicket(self, request, dto):
        """

        :param request:
        :param dto:
        :return:
        """

        try:
            # find the user
            tokenModel = self.daoRegistry.tokensDao.getToken(dto.access_token)

            if not tokenModel:
                return BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST

            user = self.daoRegistry.usersDao.getUserById(tokenModel.user_id)

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
                        imgModel.url = self.__image_base_url + Cryptography.simpleEncryption(str(_id).encode())
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

            self.daoRegistry.imagesDao.create(images)

            commentModel = None
            if dto.comment:
                commentModel = CommentModel()
                commentModel.id = commentId
                commentModel.user_id = user.id
                commentModel.text = dto.comment
                commentModel.ticket_id = ticket_id
                commentModel.created_date = datetime.datetime.utcnow()
                self.daoRegistry.commentsDao.create(commentModel)

            ticketModel = TicketModel()
            ticketModel.user_id = user.id
            ticketModel.id = ticket_id
            ticketModel.image_ids = image_ids
            ticketModel.address = dto.address
            ticketModel.latitude = dto.lat
            ticketModel.longitude = dto.long
            ticketModel.resolution = TicketModel.UNASIGNED
            ticketModel.created_date = datetime.datetime.utcnow()

            self.daoRegistry.ticketsDao.create(ticketModel)

            resp = dict(response=dict())

            hostname = ("https://" if request.is_secure() else "http://") + request.get_host()

            resp["response"] = {
                "id": Cryptography.simpleEncryption(str(ticket_id).encode()),
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
                "likes": 0,
                "liked_by_me": False
            }

            return resp, status.HTTP_200_OK
        except Exception as e:
            logger.error(stackTrace(e))
            return BaseError.INTERNAL_SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR

    def getTicket(self, request, dto):
        """

        :param request:
        :param dto:
        :return:
        """

        try:
            tokenModel = self.daoRegistry.tokensDao.getToken(dto.access_token)
            if not tokenModel:
                return BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST

            user = self.daoRegistry.usersDao.getUserById(tokenModel.user_id)

            if not user:
                return BaseError.USER_NOT_FOUND, status.HTTP_400_BAD_REQUEST

            ticket = self.daoRegistry.ticketsDao.getTicketById(ObjectId(dto.ticket_id), user.id)

            if not ticket:
                return BaseError.TICKET_NOT_FOUND, status.HTTP_400_BAD_REQUEST

            commentDict = self.daoRegistry.commentsDao.getCommentsForTickets([ticket.id], user.id,
                                                                             limit=self.MAX_FETCHED_COMMENTS_COUNT)

            likedByMeDict = self.daoRegistry.likesDao.getLikedByMe([ticket.id], user.id)

            hostname = ("https://" if request.is_secure() else "http://") + request.get_host()
            imagesDict = self.daoRegistry.imagesDao.getImages(ticket.image_ids, hostname)

            respDict = dict(response=dict())

            data = ticket.toDict()
            data["comments"] = commentDict.get(ticket.id)
            data["liked_by_me"] = likedByMeDict.get(ticket.id, False)
            data["images"] = imagesDict.get(ticket.id, [])

            respDict["response"]["ticket"] = TicketResponseDTO.fromDict(data)

            return respDict, 200
        except Exception as e:
            logger.error(stackTrace(e))
            return BaseError.INTERNAL_SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR

    def getMyTickets(self, request, dto):
        """

        :param request:
        :param dto:
        :return:
        """

        try:

            limit = dto.limit
            if dto.limit > self.MAX_FETCHED_TICKETS_COUNT:
                limit = self.MAX_FETCHED_TICKETS_COUNT

            if dto.offset < 0:
                return BaseError.INVALID_OFFSET, status.HTTP_400_BAD_REQUEST

            tokenModel = self.daoRegistry.tokensDao.getToken(dto.access_token)
            if not tokenModel:
                return BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST

            user = self.daoRegistry.usersDao.getUserById(tokenModel.user_id)

            if not user:
                return BaseError.USER_NOT_FOUND, status.HTTP_400_BAD_REQUEST

            tickets = self.daoRegistry.ticketsDao.getMyTickets(user_id=user.id, limit=limit, offset=dto.offset)

            ticketIds = list()
            imageIds = list()
            for ticket in tickets:
                imageIds += ticket.image_ids
                ticketIds.append(ticket.id)

            commentDict = self.daoRegistry.commentsDao.getCommentsForTickets(ticketIds, user.id,
                                                                             limit=self.MAX_FETCHED_COMMENTS_COUNT)

            likedByMeDict = self.daoRegistry.likesDao.getLikedByMe(ticketIds, user.id)

            hostname = ("https://" if request.is_secure() else "http://") + request.get_host()
            imagesDict = self.daoRegistry.imagesDao.getImages(imageIds, hostname)

            respDict = dict(response=dict())

            ticketList = list()

            for ticket in tickets:
                data = ticket.toDict()
                data["comments"] = commentDict.get(ticket.id)
                data["liked_by_me"] = likedByMeDict.get(ticket.id, False)
                data["images"] = imagesDict.get(ticket.id, [])
                ticketList.append(TicketResponseDTO.fromDict(data))

            respDict["response"]["tickets"] = ticketList

            return respDict, 200
        except Exception as e:
            logger.error(stackTrace(e))
            return BaseError.INTERNAL_SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR

    def likeTicket(self, request, dto):
        """

        :param request:
        :param dto:
        :return:
        """

        try:
            tokenModel = self.daoRegistry.tokensDao.getToken(dto.access_token)
            if not tokenModel:
                return BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST

            user = self.daoRegistry.usersDao.getUserById(tokenModel.user_id)

            if not user:
                return BaseError.USER_NOT_FOUND, status.HTTP_400_BAD_REQUEST

            ticket_id = ObjectId(dto.ticket_id)
            ticket = self.daoRegistry.ticketsDao.getTicketById(ticket_id)

            if not ticket:
                return BaseError.TICKET_NOT_FOUND, status.HTTP_400_BAD_REQUEST

            likeModel = self.daoRegistry.likesDao.getLike(ticket_id, user.id)
            if dto.action_type == "like":
                if likeModel:
                    return BaseError.TICKET_ALREADY_LIKED, status.HTTP_400_BAD_REQUEST

                likeModel = LikeModel()
                likeModel.ticket_id = ticket_id
                likeModel.user_id = user.id
                likeModel.created_date = datetime.datetime.utcnow()

                self.daoRegistry.likesDao.create(likeModel)
                self.daoRegistry.ticketsDao.incrementLike(ticket_id, 1)
            elif dto.action_type == "unlike":
                if not likeModel:
                    return BaseError.TICKET_NOT_LIKED, status.HTTP_400_BAD_REQUEST

                self.daoRegistry.likesDao.deleteLike(likeModel.id)
                self.daoRegistry.ticketsDao.incrementLike(ticket_id, -1)

            return {"response": {}}, status.HTTP_200_OK
        except Exception as e:
            logger.error(stackTrace(e))
            return BaseError.INTERNAL_SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR