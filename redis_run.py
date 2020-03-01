# -*- coding: utf-8 -*-
from redis_server.api import app
from redis_server.config import API_PORT, API_HOST


def main():
    app.run(host=API_HOST, port=API_PORT, debug=True)


if __name__ == '__main__':
    main()