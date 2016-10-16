# coding=utf-8
from common.base_service import BaseService
from common.roadro_errors import BaseError
from common import http_status as status
from common.utils import stackTrace
from users.model import UserModel, TokenModel
import uuid
import logging
import datetime


logger = logging.getLogger()

class UserService(BaseService):
    """

    """

    def __init__(self, databaseConnection):
        """

        :param databaseConnection:
        """
        super(UserService, self).__init__(databaseConnection)
        self.dbConn = databaseConnection

    def registerUser(self, request, data):
        """

        :param request:
        :param data:
        :return:
        """

        if "phone" not in data:
            return BaseError.INVALID_PHONE, status.HTTP_400_BAD_REQUEST

        if not data["phone"]:
            return BaseError.INVALID_PHONE, status.HTTP_400_BAD_REQUEST

        try:


            result = self.dbConn.get_connection("users").find_one({"phone": data["phone"]})

            if not result:
                userModel = UserModel()
                userModel.phone = data["phone"]
                userModel.registration_date = datetime.datetime.utcnow()
                data = userModel.toDict()
                data.pop("_id")
                result = self.dbConn.get_connection("users").insert_one(data)
                user_id = result.inserted_id

                tokenModel = TokenModel()
                tokenModel.user_id = user_id
                tokenModel.token = uuid.uuid4().hex
                tokenModel.device = "phone"
                tokenModel.created_date = datetime.datetime.utcnow()
                tokenModel.last_ip_used = request.META["REMOTE_ADDR"]
                tokenData = tokenModel.toDict()
                tokenData.pop("_id")
                self.dbConn.get_connection("tokens").insert(tokenData)

                resp = dict(response=dict())
                resp["response"]["user_id"] = str(user_id)
                resp["response"]["access_token"] = tokenModel.token

                return resp, status.HTTP_200_OK
            else:
                userModel = UserModel.fromDict(result)
                token = self.dbConn.get_connection("tokens").find_one({"user_id": result["_id"]})
                access_token = TokenModel.fromDict(token).token
                if not token:
                    tokenModel = TokenModel()
                    tokenModel.user_id = result["_id"]
                    tokenModel.token = uuid.uuid4().hex
                    tokenModel.device = "phone"
                    tokenModel.created_date = datetime.datetime.utcnow()
                    tokenModel.last_ip_used = request.META["REMOTE_ADDR"]
                    tokenData = tokenModel.toDict()
                    tokenData.pop("_id")
                    self.dbConn.get_connection("tokens").insert(tokenData)
                    access_token = tokenModel.token

                resp = dict(response=dict())
                resp["response"]["user_id"] = str(userModel.id)
                resp["response"]["access_token"] = access_token

                return resp, status.HTTP_200_OK
        except Exception as e:
            logger.error(stackTrace(e))
            return BaseError.INTERNAL_SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR