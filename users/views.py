# coding=utf-8
from common.base_view import BaseView
from common.utils import stackTrace
from users.serializers import RegisterUserRequestValidator
import logging
import ujson

logger = logging.getLogger(__name__)


class RegistrationView(BaseView):
    """
    class to be used for registration api
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

        try:
            data = ujson.loads(request.body)
        except Exception as e:
            logger.error(stackTrace(e))

        dto = RegisterUserRequestValidator.fromDict(data)

        if type(dto) is tuple:
            return self.render_json_response(dto[0], dto[1])

        httpResp = request.userService.registerUser(request, dto)

        return self.render_json_response(httpResp[0], httpResp[1])

