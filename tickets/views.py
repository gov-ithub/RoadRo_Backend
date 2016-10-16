# coding=utf-8
from common.base_view import BaseView
from common.utils import stackTrace
from common.roadro_errors import BaseError
from common import http_status as status
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
            return self.render_json_response(BaseError.INTERNAL_SERVER_ERROR, status.HTTP_500_INTERNAL_SERVER_ERROR)

        httpResp = request.ticketService.createTicket(request, data)

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
        data.update(kwargs)
        for key in request.GET:
            data[key] = request.GET.get(key)

        httpResp = request.ticketService.getTicket(request, data)

        return self.render_json_response(httpResp[0], statusCode=httpResp[1])


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

        data.update(kwargs)

        httpResp = request.ticketService.getMyTickets(request, data)

        return self.render_json_response(httpResp[0], httpResp[1])