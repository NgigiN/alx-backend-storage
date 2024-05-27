#!/usr/bin/env python3
"""Writing strings to Redis"""


import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that increments a counter each
     time the decorated method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator that stores the history of inputs
       and outputs for a function."""
    @wraps(method)
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, output)
        return output
    return wrapper


class Cache:
    """A class for storing cache information passed to the class in REdis."""

    def __init__(self):
        """Initializes a Cache object with a Redis instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in Redis and returns a key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str,
                                                          bytes, int, None]:
        """Retrieves data from Redis using the given key."""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieves a string from Redis using the given key."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieves an integer from Redis using the given key."""
        return self.get(key, fn=int)


def replay(cache_cls: Cache):
    """Displays the history of calls for a function."""
    input_key = "{}:inputs".format(cache_cls.store.__qualname__)
    output_key = "{}:outputs".format(cache_cls.store.__qualname__)

    inputs = cache_cls._redis.lrange(input_key, 0, -1)
    outputs = cache_cls._redis.lrange(output_key, 0, -1)

    print(f"{cache_cls.store.__qualname__} was called {len(inputs)} times:")
    for args, output in zip(inputs, outputs):
        args = eval(args.decode())
        print(f"{cache_cls.store.__qualname__}(*{args}) -> {output.decode()}")
