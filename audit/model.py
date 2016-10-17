# coding=utf-8


class AuditModel(object):
    """

    """

    collection = "audit"

    ID = "_id"
    USER_ID = "user_id"
    ACTION = "action"
    DATE = "date"
    TABLE = "collection"
    DATA = "data"

    def __init__(self):
        """
        """
        self.id = None
        self.user_id = None
        self.action = None
        self.date = None
        self.table = None
        self.data = None

    def toDict(self):
        """

        :return:
        """

        dictModel = dict()

        dictModel[self.ID] = self.id
        dictModel[self.USER_ID] = self.user_id
        dictModel[self.ACTION] = self.action
        dictModel[self.DATE] = self.date
        dictModel[self.TABLE] = self.table
        dictModel[self.DATA] = self.data

        return dictModel

    @classmethod
    def fromDict(cls, dictModel):
        """

        :return:
        """

        model = AuditModel()
        model.id = dictModel.get(cls.ID)
        model.user_id = dictModel.get(cls.USER_ID)
        model.action = dictModel.get(cls.ACTION)
        model.date = dictModel.get(cls.DATE)
        model.table = dictModel.get(cls.TABLE)
        model.data = dictModel.get(cls.DATA)

        return model