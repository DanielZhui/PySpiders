from flask import Flask

app = Flask(__name__)


@app.route('/api/proxyip', methods=['GET'])
def get_proxy_ip():
    return 'proxy ip'


app.run()
