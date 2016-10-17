# coding=utf-8
from common.utils import stackTrace
from common.base_cache import BaseCache
import logging



logger = logging.getLogger(__name__)


class TicketLimiter(BaseCache):
    """

    """

    def __init__(self, redis_url, max_connections, expire_time):
        """

        :param redis_url:
        :param max_connections:
        """

        super(TicketLimiter, self).__init__(redis_url, max_connections)
        self.prefix = "tl_%s"
        self.expire_time = expire_time

    def get(self, access_token):
        """

        :param access_token:
        :return:
        """

        try:
            val = self._client.get(self.prefix % access_token)
            return val
        except Exception as e:
            logger.error(stackTrace(e))
            return None

    def set(self, access_token):
        """

        :param access_token:
        :param time_limit:
        :return:
        """
        try:
            self._client.setex(self.prefix % access_token, 1, self.expire_time)
        except Exception as e:
            logger.error(stackTrace(e))