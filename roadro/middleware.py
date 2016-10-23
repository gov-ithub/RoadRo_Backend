# coding=utf-8
import ujson
from django.http import HttpResponse, HttpResponseNotFound
from common.roadro_errors import BaseError
from common.dao_registry import DaoRegistry
from users.services import UserService
from users.dao import UsersDao, TokensDao
from tickets.dao import TicketsDao, CommentsDao, LikesDao
from tickets.services import TicketService
from tickets.ticket_limiter import TicketLimiter
from common.mongo_connection import MongoConnection
from roadro import settings as projSettings
from imgserv.dao import ImagesDao

class SpringInitializer(object):
    """
    class used to initialize the spring objects and to insert the container object into the request
    """

    # Init flag
    def __init__(self, get_response):
        """

        :param get_response:
        """

        self.get_response = get_response

        self.initOk = False

        storagePath = projSettings.MEDIA_STORAGE_FOLDER

        self.__dbConn = MongoConnection()
        usersDao = UsersDao(self.__dbConn)
        ticketsDao = TicketsDao(self.__dbConn)
        tokensDao = TokensDao(self.__dbConn)
        commentsDao = CommentsDao(self.__dbConn)
        likesDao = LikesDao(self.__dbConn)
        imagesDao = ImagesDao(self.__dbConn)

        daoRegistry = DaoRegistry()
        daoRegistry.usersDao = usersDao
        daoRegistry.ticketsDao = ticketsDao
        daoRegistry.tokensDao = tokensDao
        daoRegistry.commentsDao = commentsDao
        daoRegistry.likesDao = likesDao
        daoRegistry.imagesDao = imagesDao

        self.__userService = UserService(daoRegistry)
        self.__ticketService = TicketService(daoRegistry, "/images/", storagePath)
        self.__ticketLimiter = TicketLimiter(projSettings.REDIS_URL,
                                             projSettings.REDIS_POOL_MAX_CONNECTIONS,
                                             projSettings.TICKET_LIMITER_EXPIRE_TIME)

        self.initOk = True

    def __call__(self, request):
        """
        inserts the container inside the request
        :param request: the HTTP request , on which we add the spring container
        :return: None
        """

        resp = None

        if self.initOk is False:
            # Not initialized or error during init
            resp = HttpResponse(status=502, content="Bad spring configuration")

        if not resp:
            request.userService = self.__userService
            request.ticketService = self.__ticketService
            request.ticketLimiter = self.__ticketLimiter
            resp = self.get_response(request)

        if type(resp) is HttpResponseNotFound:
            resp.content = ujson.dumps(BaseError.RESOURCE_NOT_FOUND)
            resp['Content-Length'] = len(resp.content)

        return resp