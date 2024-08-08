

import redis
import json

class CacheManager:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

    def get_cache(self, key):
        return self.redis_client.get(key)

    def set_cache(self, key, value, expiry=None):
        self.redis_client.set(key, value, ex=expiry)

    def delete_cache(self, key):
        self.redis_client.delete(key)
