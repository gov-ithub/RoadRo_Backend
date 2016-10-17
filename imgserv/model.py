

class ImageModel(object):
    """

    """

    ID = "_id"
    USER_ID = "user_id"
    URL = "url"
    METADATA = "metadata"
    WIDTH = "width"
    HEIGHT = "height"
    TICKET_ID = "ticket_id"
    MIMETYPE = "mimetype"

    collection = "images"

    def __init__(self):
        """
        """
        self.id = None
        self.user_id = None
        self.url = None
        self.metadata = None
        self.width = None
        self.height = None
        self.ticket_id = None
        self.mimetype = None

    def toDict(self):
        """

        :return:
        """

        dictModel = dict()

        dictModel[self.ID] = self.id
        dictModel[self.USER_ID] = self.user_id
        dictModel[self.URL] = self.url
        dictModel[self.METADATA] = self.metadata
        dictModel[self.WIDTH] = self.width
        dictModel[self.HEIGHT] = self.height
        dictModel[self.TICKET_ID] = self.ticket_id
        dictModel[self.MIMETYPE] = self.mimetype

        return dictModel

    @classmethod
    def fromDict(cls, dictModel):
        """

        :return:
        """

        model = ImageModel()
        model.id = dictModel.get(cls.ID)
        model.url = dictModel.get(cls.URL)
        model.metadata = dictModel.get(cls.METADATA)
        model.width = dictModel.get(cls.WIDTH)
        model.height = dictModel.get(cls.HEIGHT)
        model.ticket_id = dictModel.get(cls.TICKET_ID)
        model.user_id = dictModel.get(cls.USER_ID)
        model.mimetype = dictModel.get(cls.MIMETYPE)

        return model