#!/usr/bin/env python3
"""
Creating a Cache class in Redis
"""
import redis
from uuid import uuid4
from typing import Union, Callable

def count_calls(method : Callable ) -> Callable:
    key = method.__qualname__
    @wraps(method)
    def wrapper(*args, **kwds):
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper

def call_history(method : Callable) -> Callable:
    inputKey = method.__qualname__ + ":inputs"
    output = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Storing inputs and outputs into lists"""
        self._redis.rpush(inputKey, str(args))
        self._redis.rpush(output, str(method(self, *args, **kwds)))
        return data
    return wrapper


class Cache:
    """
    Cache cls
    """
    def __init__(self, host='localhost', port=6379):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        ki = str(uuid4())
        self._redis.set(ki, data)
        return ki 
    

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












































































































































































        
