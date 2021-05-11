from flask import Flask

from . import config
from .models import db


def create_flask_app():
    flask_app = Flask(__name__)

    # Initializing MongoDB Connection
    flask_app.config['MONGODB_SETTINGS'] = {'host': config.MONGODB_CONNECTION_STRING}
    db.init_app(flask_app)

    return flask_app
