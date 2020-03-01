# -*- coding: utf-8 -*-
"""
flask提供代理的增删接口
需要nginx部署，保证redis能被访问，才能进行对应的增删操作
"""
from flask import Flask, g
from flask import request

from redis_server.db import RedisClient

__all__ = ['app']
app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):  # 用于判断对象是否包含对应的属性
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    return '<h1><p  style="width: 100%;height: 45px;display: block;line-height: 45px;text-align: center;">欢迎来到华东的代理池系统</p></h1>'


@app.route('/put')
def upload_proxy():
    """ 将proxy上传到redis数据库中 """
    conn = get_conn()
    proxy = request.args.get("proxy")
    name = request.args.get("name")
    # remote_ip = request.remote_addr
    # port = proxy.split(":")[1]
    proxy = "{}".format(proxy)
    if not proxy:
        return "上传代理不能为空"
    conn.add(name, proxy)
    return "已成功上传代理: {}".format(proxy)


@app.route('/remove')
def remove_proxy():
    """ 删除redis中的代理 """
    conn = get_conn()
    name = request.args.get("name")
    if not name:
        return "键不能为空"
    conn.remove(name)
    return "已成功删除代理:{}".format(name)


@app.route('/random')
def random_proxy():
    """
    随机获取可用代理
    :return: redis里面的代理IP
    """
    connection = get_conn()
    return connection.random()


if __name__ == '__main__':
    app.run()