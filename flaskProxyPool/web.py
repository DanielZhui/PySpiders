import redis
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

rdb = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

app = Flask(__name__)


@app.route('/api/proxyip', methods=['GET'])
def get_proxy_ip():
    rdb.set('key', 'value')
    print(rdb.get('key').decode())
    return 'proxy ip'


if __name__ == "__main__":
    app.run()
