#!/usr/bin/env python3
"""
Creating a Cache class in Redis
"""
import redis
from uuid import uuid4
from typing import Union, Callable
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """ counts how many times methods of the Cache class are called"""
    key = method.__qualname__
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """wrapped function that increments the key"""
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Calls a method that stores the history of inputs and outputs
       for a particular function.
    """
    qualified_name = method.__qualname__
    input_key = qualified_name + ":inputs"
    output_key = qualified_name + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Stores the data in a redis db"""
        self._redis.rpush(input_key, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(output_key, str(data))
        return data
    return wrapper

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












































































































































































        
