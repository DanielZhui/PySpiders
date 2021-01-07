import redis
import json
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

from crawler.crawler import GetIpProxyPool

url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
rdb = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

app = Flask(__name__)


@app.route('/api/proxyip', methods=['GET'])
def get_proxy_ip():
    ip_list = rdb.get('ip_list')
    return ip_list


if __name__ == "__main__":
    import sys
    print(sys.path)
    # proxy_pool = GetIpProxyPool(url)
    # ip_list = proxy_pool.validate_ip()
    app.run()

# import sys
# print(sys.path)
# proxy_pool = GetIpProxyPool(url)
# ip_list = proxy_pool.validate_ip()
# app.run()
