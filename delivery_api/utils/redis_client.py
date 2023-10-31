import os
from typing import Any

import redis


class RedisClient:
    """
    Redis client to connect to the cache feature store
    """

    def __init__(self) -> None:
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = int(os.getenv("REDIS_PORT", "6379"))
        self.client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def get(self, key: str) -> Any:
        """
        Request values added to redis
        :param key:
        :return: value:
        """
        value = self.client.get(key)
        return value
