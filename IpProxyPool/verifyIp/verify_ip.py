import os
import json
import requests
import time
from settings import *


class VerifyIp(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'
    }
    file_path = os.path.join(os.path.dirname(__file__), 'useful.txt')
    def __init__(self):
        self.f = open(self.file_path)

    def test_single_ip(self):
        for line in self.f.readlines():
            line = json.loads(line)
            protocol_type = line.get('type')
            host = line.get('host')
            port = line.get('port')
            real_ip = '{}://{}:{}'.format(protocol_type, host, port)
            print('正在测试ip：', real_ip)
            with requests.get(TEST_URL, headers=self.headers, proxies={protocol_type: real_ip}, timeout=10) as response:
                if response.status_code not in SUCCESS_CODES:
                    print('>>>{}无效ip'.format(real_ip))
                else:
                    print('success>>>{} ip有效'.format(real_ip))

verify_ip = VerifyIp()
verify_ip.test_single_ip()