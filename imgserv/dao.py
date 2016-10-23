from imgserv.model import ImageModel


class ImagesDao(object):
    """

    """

    def __init__(self, db_connection):
        """

        :param db_connection:
        """
        self.dbConn = db_connection.get_connection(ImageModel)

    def create(self, imgList):
        """

        :param imgList:
        :return:
        """
        if type(imgList) is not list:
            raise ValueError("The imgList param is not a list of ImageModel objects")

        self.dbConn.insert(imgList)

    def getImages(self, imageIds, hostname=""):
        """

        :param imageIds:
        :param hostname:
        :return:
        """

        images = self.dbConn.find({ImageModel.ID: {"$in": imageIds}})

        respDict = dict()

        for image in images:
            # fix host names
            image[ImageModel.URL] = hostname + image[ImageModel.URL]
            if ImageModel.METADATA in image and "url" in image[ImageModel.METADATA]:
                image[ImageModel.METADATA]["url"] = hostname + image[ImageModel.METADATA]["url"]

            if image[ImageModel.TICKET_ID] in respDict:
                respDict[image[ImageModel.TICKET_ID]].append(image)
            else:
                respDict[image[ImageModel.TICKET_ID]] = [image]

        return respDict