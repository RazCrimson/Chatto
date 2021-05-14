from app import create_flask_app, config, socket_io

flask_app = create_flask_app()

if __name__ == '__main__':
    socket_io.run(flask_app)
