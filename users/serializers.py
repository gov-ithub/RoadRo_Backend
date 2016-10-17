# coding=utf-8
from common.base_serializer import RequestDTOValidator, ItemValidator
from common.utils import isStringNotEmpty, isString
from common.roadro_errors import BaseError
from common import http_status as status
from common import roadro_limits

class RegisterUserRequestValidator(RequestDTOValidator):
    """

    """
    rulesDict = {
        "phone": ItemValidator(funcList=[isString, str.strip, isStringNotEmpty],
                               errorCode=(BaseError.INVALID_PHONE, status.HTTP_400_BAD_REQUEST),
                               funcLimits=[(
                                   len,
                                   roadro_limits.MAX_PHONE_LENGTH,
                                   (BaseError.INVALID_PHONE, status.HTTP_400_BAD_REQUEST)
                               )]),
        "device_id": ItemValidator(funcList=[isString, str.strip, isStringNotEmpty],
                                   errorCode=(BaseError.INVALID_DEVICE_ID, status.HTTP_400_BAD_REQUEST),
                                   funcLimits=[(
                                       len,
                                       roadro_limits.MAX_DEVICE_ID,
                                       (BaseError.INVALID_DEVICE_ID, status.HTTP_400_BAD_REQUEST)
                                   )])
    }

    def __init__(self):
        """

        """
        super(RegisterUserRequestValidator, self).__init__()

        self.phone = None
        self.device_id = None