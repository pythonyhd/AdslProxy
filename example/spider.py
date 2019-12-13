# -*- coding: utf-8 -*-
# @Time    : 2019/12/13 11:17
# @Author  : King life
# @Email   : 18353626676@163.com
# @File    : spider.py
# @Software: PyCharm
import random

import redis
import requests
from fake_useragent import UserAgent

pool = redis.ConnectionPool(host="localhost", port=6379, db=15, password='admin')
redis_client = redis.Redis(connection_pool=pool, decode_responses=True)
REDIS_KEY = "proxies"
headers = {'User-Agent': UserAgent().random}


def get_proxy_from_redis():
    proxy_list = redis_client.hvals(REDIS_KEY)
    proxy = random.choice(proxy_list).decode('utf-8')
    proxies = {
        'http': 'http://martindu:fy1812!!@{}'.format(proxy),
        'https': 'https://martindu:fy1812!!@{}'.format(proxy),
    }

    return proxies


def crawler(url):
    res = requests.get(url=url, headers=headers, proxies=proxies)
    print(res.text)


if __name__ == '__main__':
    proxies = get_proxy_from_redis()
    print(proxies)
    crawler('https://www.baidu.com/')