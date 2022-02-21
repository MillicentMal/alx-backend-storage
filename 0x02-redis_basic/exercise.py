#!/usr/bin/env python3
"""
Creating a Cache class in Redis
"""


import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ counts calls of methods of the Cache"""
    key = method.__qualname__
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """wraps incrementation of key"""
        self._redis.incr(key)
        data = method(self, *args, **kwds)
        return data
    return wrapper


def call_history(method: Callable) -> Callable:
    """Keeps track of input/output of method.
    """
    method_name = method.__qualname__
    inputKey = method_name + ":inputs"
    output = method_name + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Stores the data io data"""
        self._redis.rpush(inputKey, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(output, str(data))
        return data
    return wrapper


def replay(method: Callable) -> None:
    """number of calls of func"""
    redis = method.__self__._redis
    method_name = method.__qualname__
    calls = redis.get(method_name).decode("utf-8")
    print("{} was called {} times:".format(method_name, calls))
    inputKey = method_name + ":inputs"
    output = method_name + ":outputs"
    input_list = redis.lrange(inputKey, 0, -1)
    output_list = redis.lrange(output, 0, -1)
    io_list = list(zip(input_list, output_list))
    for key, value in io_list:
        key = key.decode("utf-8")
        value = value.decode("utf-8")
        print("{}(*{}) -> {}".format(method_name, key, value))


class Cache:
    """
    Cache cls
    """
    def __init__(self, host='localhost', port=6379):
        self._redis = redis.Redis()
        self._redis.flushdb()


    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        adds a key, valu pair
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key
    

    def get(self, key: str, fn: Callable=None) -> str:
        if fn is not None:
            return fn(self._redis.get(key))
        else:
            return self._redis.get(key)

    
    def get_str(self, key: str) -> str:
        """
        Converting something to a string
        """
        return self._redis.get(key).decode("utf-8")

    
    def get_int(self, key: str) -> int:
        """Parametizes to int"""
        try:
            data = int(value.decode("utf-8"))
        except Exception:
            data = 0
        return data
