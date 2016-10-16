# coding=utf-8
import ujson
import os
from django.http import HttpResponse, HttpResponseNotFound
from common.roadro_errors import BaseError
from users.services import UserService
from tickets.services import TicketService
from common.mongo_connection import MongoConnection

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

        storagePath = os.path.abspath(os.path.dirname(__file__) + "/../media/") + "/"

        self.__dbConn = MongoConnection()
        self.__userService = UserService(self.__dbConn)
        self.__ticketService = TicketService(self.__dbConn, "http://localhost:9000/images/", storagePath)

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
            resp = self.get_response(request)

        if type(resp) is HttpResponseNotFound:
            resp.content = ujson.dumps(BaseError.RESOURCE_NOT_FOUND)
            resp['Content-Length'] = len(resp.content)

        return resp