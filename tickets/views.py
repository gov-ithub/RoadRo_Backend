# coding=utf-8
from common.base_view import BaseView
from common.utils import stackTrace
from common.roadro_errors import BaseError
from common import http_status as status
from tickets.serializers import CreateTicketRequestValidator, GetMyTicketsRequestValidator, LikeTicketRequestValidator
from tickets.serializers import GetTicketByIdRequestValidator
import logging
import ujson


logger = logging.getLogger(__name__)


class CreateTicketView(BaseView):
    """
    class to handle tickets
    """

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        try:
            data = ujson.loads(request.body)
        except Exception as e:
            logger.error(stackTrace(e))
            return self.render_json_response(BaseError.INVALID_REQUEST, status.HTTP_400_BAD_REQUEST)

        dto = CreateTicketRequestValidator.fromDict(data)
        if type(dto) is tuple:
            return self.render_json_response(dto[0], dto[1])

        if request.ticketLimiter.get(dto.access_token):
            return self.render_json_response(BaseError.CREATE_TICKET_TOO_SOON, status.HTTP_400_BAD_REQUEST)

        httpResp = request.ticketService.createTicket(request, dto)

        request.ticketLimiter.set(dto.access_token)

        return self.render_json_response(httpResp[0], statusCode=httpResp[1])


class GetTicketView(BaseView):
    """
    class to handle ticket by id
    """

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = dict()
        access_token = request.META.get("HTTP_AUTHORIZATION")
        if not access_token:
            return self.render_json_response(BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST)

        data["access_token"] = access_token
        data.update(kwargs)

        dto = GetTicketByIdRequestValidator.fromDict(data)
        if type(dto) is tuple:
            return self.render_json_response(dto[0], dto[1])

        httpResp = request.ticketService.getTicket(request, dto)

        return self.render_json_response(httpResp[0], httpResp[1])


class GetMyTicketsView(BaseView):
    """

    """

    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        """
        get my tickets
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        data = dict()
        access_token = request.META.get("HTTP_AUTHORIZATION")
        if not access_token:
            return self.render_json_response(BaseError.INVALID_TOKEN, status.HTTP_400_BAD_REQUEST)

        data["access_token"] = access_token

        dto = GetMyTicketsRequestValidator.fromDict(data)
        if type(dto) is tuple:
            return self.render_json_response(dto[0], dto[1])

        httpResp = request.ticketService.getMyTickets(request, dto)

        return self.render_json_response(httpResp[0], httpResp[1])


class LikeTicketView(BaseView):
    """

    """

    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        data = dict()
        data.update(kwargs)

        try:
            data.update(ujson.loads(request.body))
        except Exception as e:
            logger.debug(stackTrace(e))
            return self.render_json_response(BaseError.INVALID_REQUEST, status.HTTP_400_BAD_REQUEST)

        dto = LikeTicketRequestValidator.fromDict(data)

        if type(dto) is tuple:
            return self.render_json_response(dto[0], dto[1])

        resp = request.ticketService.likeTicket(request, dto)

        return self.render_json_response(resp[0], resp[1])