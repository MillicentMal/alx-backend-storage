#!/usr/bin/env python3
"""
Creating a Cache class in Redis
"""
import redis
from uuid import uuid4


class Cache:
    """
    Cache cls
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data) -> str:
        ki = str(uuid4())
        self._redis.set(ki, data)
        return ki 

cache = Cache()

data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))
















































































































































































        
