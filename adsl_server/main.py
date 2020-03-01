# -*- coding: utf-8 -*-
import re
import platform
import time

import requests
from requests.exceptions import ConnectionError, ConnectTimeout, ReadTimeout
from fake_useragent import UserAgent

from adsl_server.settings import ADSL_NETMASK, TEST_URL, TEST_TIMEOUT, VALID_STATUS_CODES, CLIENT_NAME, ADSL_BASH, \
    PROXY_PORT, USER_NAME, PASSWORD, REDIS_URI, ADSL_ERROR_CYCLE, ADSL_CYCLE, ADSL_KEEP_USE

if platform.python_version().startswith('2.'):
    import commands as subprocess
elif platform.python_version().startswith('3.'):
    import subprocess
else:
    raise ValueError('python version must be 2 or 3')


class SenderAdsl(object):
    
    def get_ip(self, netname=ADSL_NETMASK):
        """
        获取拨号IP
        :param netname: 网卡名称
        :return: 拨号ip
        """
        (status, output) = subprocess.getstatusoutput('ifconfig')
        if status == 0:
            pattern = re.compile(netname + '.*?inet.*?(\d+\.\d+\.\d+\.\d+).*?netmask', re.S)
            result = re.search(pattern, output)
            if result:
                ip = result.group(1)
                return ip
            
    def test_proxy(self, proxy):
        """
        测试代理
        :param proxy: 代理
        :return: 测试结果
        """
        proxies = {
            'http': 'http://{}:{}@{}:{}'.format(USER_NAME, PASSWORD, proxy, PROXY_PORT),
            'https': 'https://{}:{}@{}:{}'.format(USER_NAME, PASSWORD, proxy, PROXY_PORT),
        }
        headers = {'User-Agent': UserAgent().random}
        try:
            response = requests.get(url=TEST_URL, headers=headers, proxies=proxies, timeout=TEST_TIMEOUT)
            if response.status_code in VALID_STATUS_CODES:
                # print(response.text)
                return True
        except (ConnectTimeout, ReadTimeout, ConnectionError):
            return False

    def remove_proxy(self):
        """ 移除代理 """
        url = '{}/remove?name={}'.format(REDIS_URI, CLIENT_NAME)
        res = requests.get(url=url)
        print(res.text)

    def add_proxy(self, proxy):
        """ 添加代理 """
        url = '{}/put?name={}&proxy={}'.format(REDIS_URI, CLIENT_NAME, proxy)
        res = requests.get(url=url)
        print(res.text)

    def adsl(self):
        """
        拨号主进程
        ADSL代码优化，保证拨号前把IP删掉，
        确保入库的IP在拨号前都是可用的。
        执行删除后再次休眠10秒，确保取出来的IP最少能用10秒
        """
        while True:
            try:
                self.remove_proxy()
                # 删除之后再次休眠10秒，万一在刚要拨号的时候取到那个IP，那么取出来就拨号了，IP直接不能使用
                # 再次休眠确保即使已经删除，取到之后还能用，但是删除后会有一段时间没有IP进来，所以需要开尽可能多的服务器
                # 确保池子里面有IP可用
                time.sleep(ADSL_KEEP_USE)
            except:
                while True:
                    (status, output) = subprocess.getstatusoutput(ADSL_BASH)
                    if status == 0:
                        self.remove_proxy()
                        break
            (status, output) = subprocess.getstatusoutput(ADSL_BASH)
            if status == 0:
                print('ADSL拨号成功')
                ip = self.get_ip()
                if ip:
                    if self.test_proxy(ip):
                        proxies = str(ip) + ":" + PROXY_PORT
                        self.add_proxy(proxies)
                        time.sleep(ADSL_CYCLE)
                    else:
                        print('代理IP不可用，测试不通过，上次已经拨号成功的IP已经不可用，删除')
                        self.remove_proxy()
                else:
                    print('没有匹配到IP')
                    time.sleep(ADSL_ERROR_CYCLE)
            else:
                print('ADSL拨号失败')
                time.sleep(ADSL_ERROR_CYCLE)
                self.adsl()


if __name__ == '__main__':
    conn = SenderAdsl()
    conn.adsl()