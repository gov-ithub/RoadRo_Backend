# coding=utf-8

from common.base_serializer import RequestDTOValidator, ItemValidator, ItemConverter, DTOConverter
from common.utils import isStringNotEmpty, isString, safeToFloat, isNotNone, safeToInt
from common.cryptography import Cryptography
from common.roadro_errors import BaseError
from common import http_status as status
from common import roadro_limits


class MetadataDTO(DTOConverter):
    """

    """

    stringifyDict = {
        "url": ItemConverter(),
        "width": ItemConverter(),
        "height": ItemConverter()
    }

class ImageResponseDTO(DTOConverter):
    """

    """

    stringifyDict = {
        "url": ItemConverter(externalName="orig_url"),
        "metadata": ItemConverter(externalName="thumb", objType=ItemConverter.SINGLE, itemClass=MetadataDTO),
        "height": ItemConverter(optional=True),
        "width": ItemConverter(optional=True),
    }