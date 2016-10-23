# coding=utf-8

from common.base_serializer import RequestDTOValidator, ItemValidator, ItemConverter, DTOConverter
from common.utils import isStringNotEmpty, isString, safeToFloat, isNotNone, safeToInt, encode, likeActionChoice
from common.cryptography import Cryptography
from common.roadro_errors import BaseError
from common import http_status as status
from common import roadro_limits
from imgserv.serializers import ImageResponseDTO


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
                                      errorCode=(BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST)),
        "limit": ItemValidator(mandatory=False, defaultValue=0, funcList=[safeToInt, isNotNone],
                               errorCode=(BaseError.INVALID_LIMIT, status.HTTP_400_BAD_REQUEST)),
        "offset": ItemValidator(mandatory=False, defaultValue=0, funcList=[safeToInt, isNotNone],
                                errorCode=(BaseError.INVALID_OFFSET, status.HTTP_400_BAD_REQUEST))

    }

    def __init__(self):
        """

        """
        super(GetMyTicketsRequestValidator, self).__init__()

        self.access_token = None
        self.limit = 0
        self.offset = 0


class GetTicketByIdRequestValidator(RequestDTOValidator):

    rulesDict = {
        "access_token": ItemValidator(funcList=[isString, str.strip, isStringNotEmpty],
                                      errorCode=(BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST)),
        "ticket_id": ItemValidator(funcList=[isStringNotEmpty, Cryptography.decryptAES_CFB],
                                   errorCode=(BaseError.INVALID_TICKET_ID, status.HTTP_400_BAD_REQUEST))
    }

    def __init__(self):
        """

        """
        super(GetTicketByIdRequestValidator, self).__init__()

        self.access_token = None
        self.ticket_id = None


class LikeTicketRequestValidator(RequestDTOValidator):

    rulesDict = {
        "access_token": ItemValidator(funcList=[isString, str.strip, isStringNotEmpty],
                                      errorCode=(BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST)),
        "ticket_id": ItemValidator(funcList=[isStringNotEmpty, Cryptography.decryptAES_CFB],
                                   errorCode=(BaseError.INVALID_TICKET_ID, status.HTTP_400_BAD_REQUEST)),
        "action_type": ItemValidator(funcList=[isStringNotEmpty, str.lower, likeActionChoice])
    }

    def __init__(self):
        """

        """
        super(LikeTicketRequestValidator, self).__init__()

        self.access_token = None
        self.ticket_id = None
        self.action_type = None


class SimpleCommentResponseDTO(DTOConverter):
    """

    """
    stringifyDict = {
        "id": ItemConverter(modifiers=[str, encode, Cryptography.simpleEncryption]),
        "user_id": ItemConverter(modifiers=[str, encode, Cryptography.simpleEncryption]),
        "text": ItemConverter(),
        "created_date": ItemConverter(),
    }

class TicketResponseDTO(DTOConverter):
    """

    """

    stringifyDict = {
        "_id": ItemConverter(externalName="id", modifiers=[str, encode, Cryptography.simpleEncryption]),
        "address": ItemConverter(),
        "user_id": ItemConverter(modifiers=[str, encode, Cryptography.simpleEncryption]),
        "lat": ItemConverter(externalName="latitude"),
        "long": ItemConverter(externalName="longitude"),
        "resolution": ItemConverter(),
        "station": ItemConverter(optional=True),
        "images": ItemConverter(objType=ItemConverter.ITERATOR, itemClass=ImageResponseDTO),
        "likes": ItemConverter(),
        "liked_by_me": ItemConverter(optional=False, default=False),
        "comments": ItemConverter(optional=False, default=[], objType=ItemConverter.ITERATOR,
                                  itemClass=SimpleCommentResponseDTO)
    }



