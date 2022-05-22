config = {}


def set_config(host, insecure_mode=True):
    global config

    config['DOMAIN'] = host.split(":")[0]

    if insecure_mode:
        config['HOST'] = f'http://{host}'
        config['WEBSOCKET'] = f'ws://{host}'
    else:
        config['HOST'] = f'https://{host}'
        config['WEBSOCKET'] = f'wss://{host}'
