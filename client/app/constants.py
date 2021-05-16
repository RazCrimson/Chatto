LOCALHOST = '127.0.0.1'
HTTP_LOCALHOST = f'http://{LOCALHOST}:5000'

DEPLOY = 'chatto.ajpk.me'
HTTPS_DEPLOY = f'https://{DEPLOY}'

config = {}


def set_config(localhost):
    global config
    if localhost:
        config['DOMAIN'] = LOCALHOST
        config['HOST'] = HTTP_LOCALHOST
    else:
        config['DOMAIN'] = DEPLOY
        config['HOST'] = HTTPS_DEPLOY
