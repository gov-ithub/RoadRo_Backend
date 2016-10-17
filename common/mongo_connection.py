# coding =utf-8

from urllib.parse import urlparse
from pymongo import MongoClient
from roadro import settings as projSettings


class MongoConnection(object):

    def __init__(self, database_url=projSettings.DATABASE_URL):
        """

        """
        db_config = urlparse(database_url)
        self.connection = MongoClient(host=db_config.hostname,
                                      port=db_config.port,
                                      connect=True)

        self.db = self.connection[db_config.path[1:]]

    def get_connection(self, model):
        """

        :param collection:
        :return:
        """

        if hasattr(model, "collection") is False:
            raise TypeError("The model %s doesn't have the collection field set" % str(model))

        if not model.collection:
            raise ValueError("The collection field of the model %s is None or empty string" % str(model))

        return self.db[model.collection]