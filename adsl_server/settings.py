# -*- coding: utf-8 -*-
# @Time    : 2019/12/11 16:09
# @Author  : King life
# @Email   : 18353626676@163.com
# @File    : settings.py
# @Software: PyCharm
"""
IP存活时间保持在10-120秒之间
"""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
需要修改的配置
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# 拨号间隔
ADSL_CYCLE = 110

# 拨号出错重试间隔
ADSL_ERROR_CYCLE = 3

# 删除之后IP还可以用10秒
ADSL_KEEP_USE = 10

# 每台拨号机对应一个名字，不同机器需要更改
CLIENT_NAME = 'adsl1'

# ADSL命令
# ADSL_BASH = 'adsl-stop;adsl-start'
ADSL_BASH = 'pppoe-stop;pppoe-start'

# 代理配置，根据squid的配置文件填写
USER_NAME = 'martindu'
PASSWORD = 'fy1812!!'
PROXY_PORT = '8881'

# 代理保存到自己公司redis接口
REDIS_URI = 'http://3.112.239.215'

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
基本不需要改的配置
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# 拨号网卡
ADSL_NETMASK = 'ppp0'

# 拨号成功后的IP检测地址
TEST_URL = 'http://httpbin.org/get'

# 测试超时时间
TEST_TIMEOUT = 20

# 遇到以下状态码，测试通过，认定为可用IP
VALID_STATUS_CODES = [200, 201, 202]