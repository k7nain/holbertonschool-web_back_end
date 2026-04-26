#!/usr/bin/env python3
"""
Cache module with Redis call history
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def call_history(method: Callable) -> Callable:
    """Stores input/output history of a function in Redis."""

    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # store input arguments
        self._redis.rpush(inputs_key, str(args))

        # call original function
        result = method(self, *args, **kwargs)

        # store output
        self._redis.rpush(outputs_key, result)

        return result

    return wrapper


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        value = self._redis.get(key)

        if value is None:
            return None

        if fn:
            return fn(value)

        return value

    def get_str(self, key: str) -> str:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        return self.get(key, fn=int)
