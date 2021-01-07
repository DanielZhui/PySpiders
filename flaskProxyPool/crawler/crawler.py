import os
import re
import json
import requests
import urllib
from lxml import etree


url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
TEST_URL = 'https://www.baidu.com'
SUCCESS_CODES = [200, 302]

class GetIpProxyPool(object):

    ping_url = 'https://blog.csdn.net/DanielJackZ/article/details/106870071'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'
    }
    file_path = os.path.join(os.path.dirname(__file__), 'res.txt')
    def __init__(self, url):
        self.url = url
        self.get_proxy_data()
        self.f = open(self.file_path)

    def get_proxy_data(self):
        result = requests.get(self.url).text
        self.store_data(result)

    def store_data(self, data):
        f = open('./res.txt', 'w+')
        f.write(data)
        f.close()

    def get_read_lines(self):
        f = open('./res.txt', 'rb')
        lines = f.readlines()
        return lines

    def validate_ip(self):
        for line in self.f.readlines():
            line = json.loads(line)
            protocol_type = line.get('type')
            host = line.get('host')
            port = line.get('port')
            real_ip = '{}://{}:{}'.format(protocol_type, host, port)
            print('正在测试ip：', real_ip)
            try:
                with requests.get(TEST_URL, headers=self.headers, proxies={protocol_type: real_ip}, timeout=10) as response:
                    if response.status_code not in SUCCESS_CODES:
                        print('>>>{}无效ip'.format(real_ip))
                    else:
                        print('success>>>{} ip有效'.format(real_ip))
            except Exception as e:
                print(e)

if __name__ == "__main__":
    proxy_pool = GetIpProxyPool(url)
    proxy_pool.validate_ip()
