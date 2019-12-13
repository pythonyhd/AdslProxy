# -*- coding: utf-8 -*-
# @Time    : 2019/12/12 19:01
# @Author  : King life
# @Email   : 18353626676@163.com
# @File    : redis_run.py
# @Software: PyCharm
from redis_server.api import app
from redis_server.config import API_PORT, API_HOST


def main():
    app.run(host=API_HOST, port=API_PORT, debug=True)


if __name__ == '__main__':
    main()