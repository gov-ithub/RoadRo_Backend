# coding=utf-8
import logging
from redis import Redis
from urllib.parse import urlparse

class RedisClient(object):
    """

    """

    def __init__(self, redis_url, max_connections=30):
        """

        :param redis_url:
        """
        super(RedisClient, self).__init__()

        redis_config = urlparse(redis_url)

        self._client = Redis(
            host=redis_config.hostname,
            port=redis_config.port,
            db=redis_config.path[1:],
            password=redis_config.password,
            socket_keepalive=True,
            socket_connect_timeout=30)

        self._client.connection_pool.max_connections = max_connections


class BaseCache(RedisClient):
    """

    """

    def __init__(self, redis_url, max_connections):
        """

        :param redis_url:
        :param max_connections:
        """

        super(BaseCache, self).__init__(redis_url, max_connections)