# coding=utf-8

class DaoRegistry(object):
    """

    """

    def __init__(self):
        """

        """

        self.__usersDao = None
        self.__ticketsDao = None
        self.__tokensDao = None
        self.__commentsDao = None
        self.__likesDao = None
        self.__imagesDao = None

    def __getUsersDao(self):
        """

        :return:
        """
        return self.__usersDao

    def __setUsersDao(self, dao):
        """

        :param dao:
        :return:
        """

        self.__usersDao = dao
        self.__usersDao.daoRegistry = self

    def __getTicketsDao(self):
        """

        :return:
        """
        return self.__ticketsDao

    def __setTicketsDao(self, dao):
        """

        :param dao:
        :return:
        """
        self.__ticketsDao = dao
        self.__ticketsDao.daoRegistry = self

    def __getTokensDao(self):
        """

        :return:
        """
        return self.__tokensDao

    def __setTokensDao(self, dao):
        """

        :param dao:
        :return:
        """
        self.__tokensDao = dao
        self.__tokensDao.daoRegistry = dao

    def __getCommentsDao(self):
        """

        :return:
        """
        return self.__commentsDao

    def __setCommentsDao(self, dao):
        """

        :param dao:
        :return:
        """
        self.__commentsDao = dao
        self.__commentsDao.daoRegistry = dao

    def __getLikesDao(self):
        """

        :return:
        """
        return self.__likesDao

    def __setLikesDao(self, dao):
        """

        :param dao:
        :return:
        """
        self.__likesDao = dao
        self.__likesDao.daoRegistry = dao

    def __getImagesDao(self):
        """

        :return:
        """
        return self.__imagesDao

    def __setImagesDao(self, dao):
        """

        :param dao:
        :return:
        """
        self.__imagesDao = dao
        self.__imagesDao.daoRegistry = dao

    # ===============================
    #       PROPERTIES
    # ===============================
    usersDao = property(__getUsersDao, __setUsersDao)
    tokensDao = property(__getTokensDao, __setTokensDao)
    ticketsDao = property(__getTicketsDao, __setTicketsDao)
    imagesDao = property(__getImagesDao, __setImagesDao)
    likesDao = property(__getLikesDao, __setLikesDao)
    commentsDao = property(__getCommentsDao, __setCommentsDao)