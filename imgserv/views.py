# coding=utf-8
import logging
from common.base_view import BaseView
from common.roadro_errors import BaseError
from common.utils import stackTrace
from common import http_status as status
from bson.objectid import ObjectId
from common.cryptography import Cryptography
from imgserv.model import ImageModel
from users.model import TokenModel

logger = logging.getLogger(__name__)


class ImgServeView(BaseView):

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        try:
            img_id = kwargs["img_id"]
            access_token = request.META.get("HTTP_AUTHORIZATION")
            if not access_token:
                return self.render_json_response(BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST)

            result = request.ticketService.dbConn.get_connection(TokenModel).find_one({"token": access_token})
            if not result:
                return self.render_json_response(BaseError.USER_NOT_FOUND, status.HTTP_400_BAD_REQUEST)

            db_id = Cryptography.decryptAES_CFB(img_id)

            if "_" in db_id:
                index = db_id.find('_')
                dbId = db_id[index+1:]
            else:
                dbId = db_id
            imgDict = request.ticketService.dbConn.get_connection(ImageModel).find_one({"_id": ObjectId(dbId),
                                                                                        "user_id": result["user_id"]})

            if not imgDict:
                return self.render_json_response(BaseError.IMAGE_NOT_FOUND, status.HTTP_400_BAD_REQUEST)

            path = "%s%s/%s/%s" % (request.ticketService.base_img_path, dbId[-2:], dbId[-4:-2], db_id)

            return self.render_file(path, imgDict["mimetype"])
        except Exception as e:
            logger.error(stackTrace(e))
            return self.render_json_response(BaseError.FILE_NOT_FOUND, status.HTTP_404_NOT_FOUND)
