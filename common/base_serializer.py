# -*- coding: utf-8 -*-
from common.utils import stackTrace
import logging

logger = logging.getLogger(__name__)


class ItemIteratorError(Exception):
    pass


class ItemConverter(object):
    """

    """

    ITERATOR = "iter"
    SINGLE = "one"

    def __init__(self, objType=None, itemClass=None, externalName=None, optional=False, default=None, modifiers=list()):
        """
        constructor
        """

        self.objType = objType
        self.itemClass = itemClass
        self.externalName = externalName
        self.optional = optional
        self.default = default
        self.modifiers = modifiers


class DTOConverter(object):
    """
    class that helps convert from a model or dict to a dto dict
    """

    stringifyDict = dict()

    @classmethod
    def fromModel(cls, model):
        """

        :param model:
        :return:
        """
        respDict = dict()

        for key in cls.stringifyDict:
            obj = None
            try:
                obj = getattr(model, key)
            except AttributeError:
                pass
            if cls.stringifyDict[key].optional is True and obj is None:
                if cls.stringifyDict[key].default is not None:
                    respDict[cls.stringifyDict[key].externalName or key] = cls.stringifyDict[key].default
                continue
            objType = cls.stringifyDict[key].objType
            externalName = cls.stringifyDict[key].externalName
            if objType is None:
                for v in cls.stringifyDict[key].modifiers:
                    obj = v(obj)
                respDict[externalName or key] = obj
            elif objType == ItemConverter.ITERATOR:
                dtoType = cls.stringifyDict[key].itemClass
                respDict[externalName or key] = list()
                for val in obj:
                    respDict[externalName or key].append(dtoType.fromModel(val))
            else:
                respDict[externalName or key] = cls.stringifyDict[key].fromModel(obj)

        return respDict

    @classmethod
    def fromDict(cls, dataDict):
        """

        :param dataDict:
        :return:
        """

        respDict = dict()
        try:
            for key in cls.stringifyDict:
                if cls.stringifyDict[key].optional is True and key not in dataDict:
                    if cls.stringifyDict[key].default is not None:
                        respDict[cls.stringifyDict[key].externalName or key] = cls.stringifyDict[key].default
                    continue
                obj = dataDict[key]
                objType = cls.stringifyDict[key].objType
                externalName = cls.stringifyDict[key].externalName
                if objType is None:
                    for v in cls.stringifyDict[key].modifiers:
                        obj = v(obj)
                    respDict[externalName or key] = obj
                elif objType == ItemConverter.ITERATOR:
                    dtoType = cls.stringifyDict[key].itemClass
                    respDict[externalName or key] = list()
                    for val in obj:
                        respDict[externalName or key].append(dtoType.fromSocrativeDict(val))
                elif objType == ItemConverter.SINGLE:
                    dtoType = cls.stringifyDict[key].itemClass
                    respDict[externalName or key] = dtoType.fromSocrativeDict(obj)
                else:
                    respDict[externalName or key] = cls.stringifyDict[key].fromSocrativeDict(obj)

            return respDict
        except Exception as e:
            logger.error(stackTrace(e))
            raise


class ItemValidator(object):

    OBJECT = 1
    LIST = 2

    def __init__(self, mandatory=True, defaultValue=None, funcList=list(), errorCode=(), iterator=False, itClass=None,
                 funcLimits=()):
        """
        :param mandatory:
        :param defaultValue:
        :param funcList:
        :param funcLimits:
        :param errorCode:
        """
        self.mandatory = mandatory
        self.defaultValue = defaultValue
        self.funcList = funcList
        self.errorCode = errorCode
        self.iterator = iterator
        self.iteratorCls = itClass
        self.funcLimits = funcLimits


class RequestDTOValidator(object):
    """
    base class to check request data
    """

    rulesDict = dict()  # key: ItemValidator

    @classmethod
    def fromDict(cls, dataDict):
        """
        :param dataDict
        :return:
        """
        dto = cls()

        for k in cls.rulesDict:
            if k in dataDict:
                if cls.rulesDict[k].iterator == ItemValidator.LIST:
                    for v in cls.rulesDict[k].funcList:
                        for obj in dataDict[k]:
                            res = v(obj)
                            if res is False:
                                raise Exception("Item %s of key %s failed validation" % (str(obj), k))
                    setattr(dto, k, list())
                    for v in dataDict[k]:
                        res = cls.rulesDict[k].iteratorCls.fromDict(v) if type(v) is dict else v
                        if type(res) is tuple and (type(res[1] is not bool or res[1] is False)):
                            return res
                        if type(res) is tuple:
                            getattr(dto, k).append(res[0])
                        else:
                            getattr(dto, k).append(res)

                    continue
                elif cls.rulesDict[k].iterator == ItemValidator.OBJECT:
                    setattr(dto, k, cls.rulesDict[k].iteratorCls())
                    temp = getattr(dto, k).fromDict(dataDict[k])
                    if type(temp) == tuple:
                        return temp
                    setattr(dto, k, temp)
                    continue

                obj = dataDict[k]
                for v in cls.rulesDict[k].funcList:
                    res = v(obj)
                    if (type(res) is tuple and type(res[1]) is bool and res[1] is False) or\
                            (type(res) is bool and res is False):
                        if len(cls.rulesDict[k].errorCode) > 0:
                            return cls.rulesDict[k].errorCode
                    elif type(res) not in (bool, tuple):
                        obj = res
                    elif type(res) is tuple:
                        obj = res[0]

                for func, limit, error in cls.rulesDict[k].funcLimits:
                    if func(obj) > limit:
                        return error

                setattr(dto, k, obj)
            elif cls.rulesDict[k].mandatory is False:
                setattr(dto, k, cls.rulesDict[k].defaultValue)
            else:
                return cls.rulesDict[k].errorCode

        return dto
