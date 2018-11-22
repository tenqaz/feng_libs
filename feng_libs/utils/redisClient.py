"""
author: jim
date: 2018-10-08

操作redis
"""

import redis

__all__ = ['RedisClient']


class RedisClient():

    def __init__(self, host="localhost", port=6379, db=0, password=None):
        if password:
            self._db = redis.Redis(host, port, db, password)
        else:
            self._db = redis.Redis(host, port)

    def keys(self, pattern="*"):
        return self._db.keys(pattern)

    def set(self, key, value):
        """
        string
        """
        return self._db.set(key, value)

    def get(self, key):
        """
        string
        """
        return self._db.get(key)

    def get_str(self, key):
        """
        string
        """
        value = self.get(key)
        return str(value, 'utf-8')

    def hset(self, key, field, value):
        """
        hash
        """
        return self._db.hset(key, field, value)

    def hget(self, key, field):
        """
        hash
        """
        return self._db.hget(key, field)

    def hget_str(self, key, field):
        """hash"""
        return str(self.hget(key, field), 'utf-8')

    def lpush(self, key, *value):
        """
        list
        """
        return self._db.lpush(key, *value)

    def lrange(self, key, start, end):
        """
        list
        """
        return self._db.lrange(key, start, end)

    def lset(self, key, index, value):
        """
        list
        """
        return self._db.lset(key, index, value)

    def sadd(self, key, *value):
        """
        set
        """
        return self._db.sadd(key, *value)

    def smembers(self, key):
        """
        set
        """
        return self._db.smembers(key)

    def zadd(self, key, *args, **kwargs):
        """
        zset
        """
        return self._db.zadd(name, score, value)


if __name__ == '__main__':
    redis = RedisClient()
    # redis.set("name", "zhangsan")
    # print(redis.keys())
    # print(redis.get("name"))
    # print(redis.get_str("name"))

    # print("-" * 30)

    # redis.hset('student', 'name', 'zhangsan')
    # redis.hset('student', 'age', '12')
    # print(redis.hget('student', 'name'))
    # print(redis.hget_str('student', 'name'))

    # print("-" * 30)

    # redis.lpush("name", "zhangsan", "lisi")
    # print(redis.lrange("name", 0, 10))

    print("-" * 30)

    redis.sadd("name", "zhangsan", "lisi")
    print(redis.smembers("name"))
