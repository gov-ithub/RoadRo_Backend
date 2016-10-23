# coding=utf-8
import logging
import ujson

logger = logging.getLogger(__name__)


def stackTrace(exception):
    """

    :param exception:
    :return:
    """
    # TODO get the stack trace

    return str(exception)


def safeToInt(obj):
    """

    :param obj:
    :return:
    """

    try:
        if obj is None:
            return None
        return int(obj)
    except Exception as e:
        logger.debug(stackTrace(e))
        return None


def safeToBool(obj):
    """

    :param obj:
    :return:
    """
    try:
        if obj is None:
            return None
        else:
            return ujson.loads(str(obj).lower()) is True
    except Exception as e:
        logger.debug(stackTrace(e))
        return None


def safeToFloat(obj):
    """

    :param obj:
    :return:
    """
    try:
        return float(obj)
    except Exception as e:
        logger.error(stackTrace(e))
        return None


def isStringNotEmpty(obj):
    """
    :param obj:
    :return:
    """
    if type(obj) is str and obj != "":
        return True
    else:
        return False


def isString(obj):
    """

    :param obj:
    :return:
    """

    return type(obj) is str


def isNotNone(obj):
    """
    :param obj:
    :return:
    """
    return obj is not None


def isBool(obj):
    """

    :param obj:
    :return:
    """
    return type(obj) is bool


def isBoolOrNone(obj):
    """

    :param obj:
    :return:
    """
    return type(obj) is bool or obj is None


def serializerToBool(obj):
    """

    :param obj:
    :return:
    """
    return safeToBool(obj), True


def encode(obj):
    """

    :param obj:
    :return:
    """
    return obj.encode()


def likeActionChoice(obj):

    if obj in ("like", "unlike"):
        return True

    return False