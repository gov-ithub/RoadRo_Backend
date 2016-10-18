# coding=utf-8

from common.base_serializer import RequestDTOValidator, ItemValidator
from common.utils import isStringNotEmpty, isString, safeToFloat, isNotNone
from common.roadro_errors import BaseError
from common import http_status as status
from common import roadro_limits


class CreateTicketRequestValidator(RequestDTOValidator):

    rulesDict = {
        "access_token": ItemValidator(funcList=[isString, str.strip, isStringNotEmpty],
                                      errorCode=(BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST)),
        "images": ItemValidator(iterator=ItemValidator.LIST, funcList=[isStringNotEmpty],
                                errorCode=(BaseError.INVALID_IMAGES_FIELD, status.HTTP_400_BAD_REQUEST),
                                funcLimits=[(
                                    len,
                                    roadro_limits.MAX_UPLOADED_IMAGES,
                                    (BaseError.TOO_MANY_IMAGES, status.HTTP_400_BAD_REQUEST))]),
        "address": ItemValidator(funcList=[isString, str.strip, isStringNotEmpty],
                                 errorCode=(BaseError.INVALID_ADDRESS_FIELD, status.HTTP_400_BAD_REQUEST),
                                 funcLimits=[(
                                     len,
                                     roadro_limits.MAX_ADDRESS_FIELD,
                                     (BaseError.STRING_TOO_LONG, status.HTTP_400_BAD_REQUEST)
                                 )]),
        "lat": ItemValidator(mandatory=False, funcList=[safeToFloat, isNotNone],
                             errorCode=(BaseError.INVALID_LATITUDE_FIELD, status.HTTP_400_BAD_REQUEST)),
        "long": ItemValidator(mandatory=False, funcList=[safeToFloat, isNotNone],
                              errorCode=(BaseError.INVALID_LONGITUDE_FIELD, status.HTTP_400_BAD_REQUEST)),
        "comment": ItemValidator(mandatory=False, funcList=[isString, str.strip, isStringNotEmpty],
                                 errorCode=(BaseError.INVALID_COMMENT_FIELD, status.HTTP_400_BAD_REQUEST),
                                 funcLimits=[(
                                     len,
                                     roadro_limits.MAX_COMMENT_SIZE,
                                     (BaseError.STRING_TOO_LONG, status.HTTP_400_BAD_REQUEST)
                                 )])

    }

    def __init__(self):
        """

        """
        super(CreateTicketRequestValidator, self).__init__()

        self.access_token = None
        self.address = None
        self.images = list()
        self.lat = None
        self.long = None
        self.comment = None


class GetMyTicketsRequestValidator(RequestDTOValidator):

    rulesDict = {
        "access_token": ItemValidator(funcList=[isString, str.strip, isStringNotEmpty],
                                      errorCode=(BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST))

    }

    def __init__(self):
        """

        """
        super(GetMyTicketsRequestValidator, self).__init__()

        self.access_token = None