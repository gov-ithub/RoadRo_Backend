# coding=utf-8


class LikeModel(object):
    """

    """

    ID = "_id"
    USER_ID = "user_id"
    TICKET_ID = "ticket_id"
    CREATED_DATE = "created_date"

    collection = "likes"

    def __init__(self):
        """
        """
        self.id = None
        self.user_id = None
        self.created_date = None
        self.ticket_id = None

    def toDict(self):
        """

        :return:
        """

        dictModel = dict()

        dictModel[self.ID] = self.id
        dictModel[self.USER_ID] = self.user_id
        dictModel[self.CREATED_DATE] = self.created_date
        dictModel[self.TICKET_ID] = self.ticket_id

        return dictModel

    @classmethod
    def fromDict(cls, dictModel):
        """

        :return:
        """

        model = TicketModel()
        model.id = dictModel.get(cls.ID)
        model.user_id = dictModel.get(cls.USER_ID)
        model.ticket_id = dictModel.get(cls.TICKET_ID)
        model.created_date = dictModel.get(cls.CREATED_DATE)

        return model


class CommentModel(object):
    """

    """
    ID = "_id"
    USER_ID = "user_id"
    TICKET_ID = "ticket_id"
    TEXT = "text"
    HIDDEN = "hidden"
    CREATED_DATE = "created_date"

    collection = "comments"

    def __init__(self):
        """
        """
        self.id = None
        self.user_id = None
        self.text = None
        self.hidden = None
        self.created_date = None
        self.ticket_id = None

    def toDict(self):
        """

        :return:
        """

        dictModel = dict()

        dictModel[self.ID] = self.id
        dictModel[self.USER_ID] = self.user_id
        dictModel[self.TEXT] = self.text
        dictModel[self.HIDDEN] = self.hidden
        dictModel[self.CREATED_DATE] = self.created_date
        dictModel[self.TICKET_ID] = self.ticket_id

        return dictModel

    @classmethod
    def fromDict(cls, dictModel):
        """

        :return:
        """

        model = TicketModel()
        model.id = dictModel.get(cls.ID)
        model.user_id = dictModel.get(cls.USER_ID)
        model.text = dictModel.get(cls.TEXT)
        model.hidden = dictModel.get(cls.HIDDEN)
        model.ticket_id = dictModel.get(cls.TICKET_ID)
        model.created_date = dictModel.get(cls.CREATED_DATE)

        return model


class TicketModel(object):
    """

    """
    ID = "_id"
    USER_ID = "user_id"
    ADDRESS = "address"
    LATITUDE = "lat"
    LONGITUDE = "long"
    RESOLUTION = "resolution"
    STATION_ID = "station_id"
    IMAGE_IDS = "image_ids"
    CREATED_DATE = "created_date"
    LAST_UPDATE = "last_update"
    LIKES = "likes"


    UNASIGNED = 0
    IN_PROGRESS = 10
    RESOLVED = 30

    collection = "tickets"

    def __init__(self):
        """
        """
        self.id = None
        self.user_id = None
        self.address = None
        self.latitude = None
        self.longitude = None
        self.resolution = None
        self.station_id = None
        self.image_ids = None
        self.created_date = None
        self.last_update = None
        self.likes = 0

    def toDict(self):
        """

        :return:
        """

        dictModel = dict()

        dictModel[self.ID] = self.id
        dictModel[self.USER_ID] = self.user_id
        dictModel[self.ADDRESS] = self.address
        dictModel[self.LATITUDE] = self.latitude
        dictModel[self.LONGITUDE] = self.longitude
        dictModel[self.RESOLUTION] = self.resolution
        dictModel[self.STATION_ID] = self.station_id
        dictModel[self.IMAGE_IDS] = self.image_ids
        dictModel[self.CREATED_DATE] = self.created_date
        dictModel[self.LAST_UPDATE] = self.last_update
        dictModel[self.LIKES] = self.likes


        return dictModel

    @classmethod
    def fromDict(cls, dictModel):
        """

        :return:
        """

        model = TicketModel()
        model.id = dictModel.get(cls.ID)
        model.address = dictModel.get(cls.ADDRESS)
        model.user_id = dictModel.get(cls.USER_ID)
        model.latitude = dictModel.get(cls.LATITUDE)
        model.longitude = dictModel.get(cls.LONGITUDE)
        model.resolution = dictModel.get(cls.RESOLUTION)
        model.station_id = dictModel.get(cls.STATION_ID)
        model.image_ids = dictModel.get(cls.IMAGE_IDS)
        model.likes = dictModel.get(cls.LIKES, 0)

        return model

