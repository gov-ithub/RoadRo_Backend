# coding=utf-8


class BaseError(object):
    """

    """

    INTERNAL_SERVER_ERROR = {"error": {"code": 800, "message": "Internal server error"}}

    MISSING_IMAGES_FIELD = {"error": {"code": 600, "message": "the images are missing"}}

    RESOURCE_NOT_FOUND = {"error": {"code": 400, "message": "page not found"}}
    USER_NOT_FOUND = {"error": {"code": 401, "message": "The user wasn't found"}}

    INVALID_PHONE = {"error": {"code": 200, "message": "the phone field is invalid"}}
    INVALID_TOKEN = {"error": {"code": 201, "message": "the token is invalid"}}
    INVALID_IMAGES_FIELD = {"error": {"code": 202, "message": "the images field is invalid"}}
    INVALID_IMAGE_STRING = {"error": {"code": 203, "message": "the image string is invalid"}}
    TOO_MANY_IMAGES = {"error": {"code": 204, "message": "there are too many images in the images field"}}
    INVALID_ADDRESS_FIELD = {"error": {"code": 205, "message": "the address field is invalid"}}
    INVALID_LATITUDE_FIELD = {"error": {"code": 206, "message": "the latitude field is invalid"}}
    INVALID_LONGITUDE_FIELD = {"error": {"code": 207, "message": "the longitude field is invalid"}}
    INVALID_COMMENT_FIELD = {"erorr": {"code": 208, "message": "The comment field is invalid"}}
    INVALID_IMAGE = {"error": {"code": 209, "message": "The image is invalid"}}

    FILE_TYPE_NOT_SUPPORTED = {"error": {"code": 0, "message": "The file type is not supported. Send only jpg or png images"}}




