from flask import Flask

from app import config
from app.models import db


def create_flask_app():
    flask_app = Flask(__name__)

    # MongoDB Config
    flask_app.config['MONGODB_DB'] = config.MONGODB_DB
    flask_app.config['MONGODB_HOST'] = config.MONGODB_HOST
    flask_app.config['MONGODB_PORT'] = config.MONGODB_PORT
    flask_app.config['MONGODB_USERNAME'] = config.MONGODB_USERNAME
    flask_app.config['MONGODB_PASSWORD'] = config.MONGODB_PASSWORD
    db.init_app(flask_app)

    return flask_app
