import re
import json
import requests
import urllib
from lxml import etree


url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'

class GetIpProxyPool(object):

    ping_url = 'https://blog.csdn.net/DanielJackZ/article/details/106870071'

    def __init__(self, url):
        self.url = url
        self.get_proxy_data()

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

    def validate_proxy(self):
        f = open('./useful.txt', 'w+')
        lines = self.get_read_lines()
        for line in lines:
            line = json.loads(line.strip())
            proxy_ip = {line.get('type'): line.get('host')}
            proxy_support = urllib.request.ProxyHandler(proxy_ip)
            opener = urllib.request.build_opener(proxy_support)
            opener.addheaders = [('User-Agent',
                                            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
            urllib.request.install_opener(opener)
            try:
                response = urllib.request.urlopen(self.ping_url, timeout=5)
            except:
                pass
            if response.read().decode('utf-8'):
                f.write(json.dumps(line) + '\n')

if __name__ == "__main__":
    proxy_pool = GetIpProxyPool(url)
    proxy_pool.validate_proxy()