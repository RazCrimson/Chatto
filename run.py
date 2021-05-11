from app import create_flask_app, config

flask_app = create_flask_app()

if __name__ == '__main__':
    flask_app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.APP_DEBUG)
