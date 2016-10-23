# coding=utf-8
from users.model import UserModel, TokenModel


class UsersDao(object):
    """

    """

    def __init__(self, db_connection):
        """

        :param db_connection:
        """

        self.dbConn = db_connection.get_connection(UserModel)

    def getUserByPhone(self, phone_hash):
        """

        :param phone_hash:
        :return:
        """

        return self.dbConn.find_one({UserModel.PHONE_HASH: phone_hash})

    def createUser(self, userModel):
        """

        :param userModel:
        :return:
        """

        data = userModel.toDict()
        if UserModel.ID in data:
            data.pop(UserModel.ID)

        result = self.dbConn.insert_one(data)

        return result.inserted_id

    def addDevice(self, user_id, device_id):
        """

        :param device_id:
        :return:
        """
        # we set the device as valid because we can't validate for now the phone number
        device = {UserModel.DEVICE_ID: device_id, UserModel.IS_VALID: True}

        self.dbConn.update({UserModel.ID: user_id}, {"$addToSet": {UserModel.DEVICES: device}})

        return user_id

    def getUserById(self, user_id):
        """

        :param user_id:
        :return:
        """

        userModelDict = self.dbConn.find_one({UserModel.ID: user_id})

        if userModelDict:
            return UserModel.fromDict(userModelDict)

        return None


class TokensDao(object):
    """

    """

    def __init__(self, db_connection):
        """

        :param db_connection:
        """

        self.dbConn = db_connection.get_connection(TokenModel)

    def create(self, tokenModel):
        """

        :param tokenModel:
        :return:
        """

        tokenData = tokenModel.toDict()
        if TokenModel.ID in tokenData:
            tokenData.pop("_id")
        self.dbConn.insert(tokenData)

    def getToken(self, access_token):
        """

        :param access_token:
        :return:
        """

        tokenModelDict = self.dbConn.find_one({TokenModel.TOKEN: access_token})

        if tokenModelDict:
            return TokenModel.fromDict(tokenModelDict)

        return None