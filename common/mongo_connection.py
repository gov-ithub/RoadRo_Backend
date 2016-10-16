# coding =utf-8

from pymongo import MongoClient

class MongoConnection(object):

    def __init__(self, database="roadro"):
        """

        """
        self.connection = MongoClient("localhost", port=27017, connect=True)
        self.db = self.connection[database]

    def get_connection(self, collection):
        """

        :param collection:
        :return:
        """

        return self.db[collection]