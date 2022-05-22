from gevent import monkey

monkey.patch_all()

from app import create_flask_app, socket_io, config

flask_app = create_flask_app()

if __name__ == '__main__':
    print(f"Starting on {config.APP_HOST}:{config.APP_PORT}")
    socket_io.run(flask_app, host=config.APP_HOST, debug=config.APP_DEBUG, port=config.APP_PORT)
