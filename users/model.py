# coding=utf-8


class UserModel(object):
    """

    """
    ID = "_id"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    PHONE = "phone"
    REGISTRATION_DATE = "registration_date"


    def __init__(self):
        """
        """
        self.id = None
        self.first_name = None
        self.last_name = None
        self.phone = None
        self.registration_date = None

    def toDict(self):
        """

        :return:
        """

        dictModel = dict()

        dictModel[self.ID] = self.id
        dictModel[self.FIRST_NAME] = self.first_name
        dictModel[self.LAST_NAME] = self.last_name
        dictModel[self.PHONE] = self.phone
        dictModel[self.REGISTRATION_DATE] = self.registration_date

        return dictModel

    @classmethod
    def fromDict(cls, dictModel):
        """

        :return:
        """

        model = UserModel()
        model.id = dictModel.get(cls.ID)
        model.first_name = dictModel.get(cls.FIRST_NAME)
        model.last_name = dictModel.get(cls.LAST_NAME)
        model.phone = dictModel.get(cls.PHONE)
        model.registration_date = dictModel.get(cls.REGISTRATION_DATE)

        return model

class TokenModel(object):
    """

    """
    ID = "_id"
    USER_ID = "user_id"
    TOKEN = "token"
    DEVICE = "device"
    CREATED_DATE = "created_date"
    LAST_IP_USED = "last_ip_used"


    def __init__(self):
        """
        """
        self.id = None
        self.user_id = None
        self.token = None
        self.device = None
        self.created_date = None
        self.last_ip_used = None

    def toDict(self):
        """

        :return:
        """

        dictModel = dict()

        dictModel[self.ID] = self.id
        dictModel[self.USER_ID] = self.user_id
        dictModel[self.TOKEN] = self.token
        dictModel[self.DEVICE] = self.device
        dictModel[self.CREATED_DATE] = self.created_date
        dictModel[self.LAST_IP_USED] = self.last_ip_used


        return dictModel

    @classmethod
    def fromDict(cls, dictModel):
        """

        :return:
        """

        model = UserModel()
        model.id = dictModel.get(cls.ID)
        model.token = dictModel.get(cls.TOKEN)
        model.user_id = dictModel.get(cls.USER_ID)
        model.device = dictModel.get(cls.DEVICE)
        model.created_date = dictModel.get(cls.CREATED_DATE)

        return model

