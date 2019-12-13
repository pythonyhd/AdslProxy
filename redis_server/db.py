# -*- coding: utf-8 -*-
# @Time    : 2019/12/11 15:52
# @Author  : King life
# @Email   : 18353626676@163.com
# @File    : db.py
# @Software: PyCharm
"""
存储器，存储拨号成功后的IP，Hash监控每台拨号机器拨号情况
"""
import random

import redis

from redis_server.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, PROXY_KEY


class RedisClient(object):
    def __init__(self):
        """
        初始化Redis连接
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis 密码
        :param db: Redis 数据库
        :param proxy_key: Redis 哈希表名
        """
        if REDIS_PASSWORD:
            self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)
        else:
            self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

        self.proxy_key = PROXY_KEY

    def add(self, name, proxy):
        """
        添加代理
        :param name:主机名
        :param proxy:代理
        :return:存储结果
        """
        return self.db.hset(self.proxy_key, name, proxy)

    def get(self, name):
        """
        获取代理
        :param name: 主机名称
        :return: 代理
        """
        return self.db.hget(self.proxy_key, name)

    def count(self):
        """
        获取代理总数
        :return: 代理总数
        """
        return self.db.hlen(self.proxy_key)

    def remove(self, name):
        """
        删除代理
        :param name: 主机名称
        :return: 删除结果
        """
        return self.db.hdel(self.proxy_key, name)

    def names(self):
        """
        获取主机名称列表
        :return:主机名称列表
        """
        return self.db.hkeys(self.proxy_key)

    def proxies(self):
        """
        获取代理列表
        :return: 代理列表
        """
        return self.db.hvals(self.proxy_key)

    def random(self):
        """
        随机获取代理
        :return:
        """
        proxies = self.proxies()
        return random.choice(proxies)

    def all(self):
        """
        获取字典
        :return:
        """
        return self.db.hgetall(self.proxy_key)
    
    
if __name__ == '__main__':
    conn = RedisClient()
    conn.add('adsl1', '81.163.123.233:8080')
    # conn.remove('adsl')