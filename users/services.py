# coding=utf-8
from common.base_service import BaseService
from common.roadro_errors import BaseError
from common import http_status as status
from common.utils import stackTrace
from common.cryptography import Cryptography
from users.model import UserModel, TokenModel
import uuid
import logging
import datetime


logger = logging.getLogger()


class UserService(BaseService):
    """

    """

    def __init__(self, daoRegistry):
        """

        :param daoRegistry:
        """
        super(UserService, self).__init__(daoRegistry)

    def registerUser(self, request, dto):
        """

        :param request:
        :param dto:
        :return:
        """

        try:

            phone_hash = Cryptography.hash(dto.phone)
            result = self.daoRegistry.usersDao.getUserByPhone(phone_hash)

            if not result:
                userModel = UserModel()
                # encrypt the phone number
                userModel.phone = Cryptography.encryptAES_CFB(dto.phone.encode())
                userModel.phone_hash = phone_hash
                userModel.registration_date = datetime.datetime.utcnow()
                userModel.devices = [{"device_id": dto.device_id, "is_valid": True}]
                userModel.role = UserModel.NORMAL_USER

                user_id = self.daoRegistry.usersDao.createUser(userModel)
            else:
                userModel = UserModel.fromDict(result)

                for deviceDict in userModel.devices:
                    if deviceDict["device_id"] == dto.device_id:
                        return BaseError.USER_ALREADY_REGISTERED, status.HTTP_400_BAD_REQUEST

                user_id = self.daoRegistry.usersDao.addDevice(userModel.id, dto.device_id)

            # do not send an access token when we can validate the phone number
            tokenModel = TokenModel()
            tokenModel.user_id = user_id
            tokenModel.token = uuid.uuid4().hex
            tokenModel.device = dto.device_id
            tokenModel.created_date = datetime.datetime.utcnow()
            tokenModel.last_ip_used = request.META["REMOTE_ADDR"]

            self.daoRegistry.tokensDao.create(tokenModel)

            resp = dict(response=dict())
            resp["response"]["user_id"] = Cryptography.encryptAES_CFB(str(userModel.id).encode())
            resp["response"]["access_token"] = tokenModel.token

            return resp, status.HTTP_200_OK
        except Exception as e:
            logger.error(stackTrace(e))
            return BaseError.INTERNAL_SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR
