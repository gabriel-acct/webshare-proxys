import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return {
            'message': 'Seja bem-vindo ao Proxy Check! Acesse /proxy-check para verificar sua proxy e IP.',
            'criador': '66999407738'
        }

@app.route('/cpaproxy', methods=['GET'])
def cpa_proxy():
    proxys = []
    all_proxy = ["885.72.241.11:7303:cpaproxyscon:cpaproxyscom"]
    for proxy in all_proxy:
        proxys.append(proxy)
    for proxy in proxys:
        try:
            proxy_form = format_proxy(proxy)
            r = requests.get('https://httpbin.org/ip', proxies=proxy_form)
            return {
                'status': True,
                'proxy': proxy,
                'response': r.json(),
                'criador': 'CPAPROXYS',
            }
        except Exception as e:
            return {
                'status': False,
                'error': str(e),
                'message': 'Proxy is not working'
            }

def format_proxy(proxy: str) -> dict:
    ip, port, user, password = proxy.split(':')
    proxy = f"http://{user}:{password}@{ip}:{port}"
    return{
        "http": proxy,
        "https": proxy
    }

@app.route('/proxy-check', methods=['GET'])
def check():
    if request.headers.get('X-Forwarded-For'):
        return {
            'status': True,
            'client_ip': request.headers.get('X-Forwarded-For')
        }
    else:
        return {
            'status': False,
            'client_ip': request.remote_addr
        }
    return 'Proxy Check'

if __name__ == '__main__':
    app.run(debug=True)