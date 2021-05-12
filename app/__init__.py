from datetime import timedelta

from flask import Flask
from flask_bcrypt import Bcrypt

from . import config
from .authentication import jwt
from .models import db


def create_flask_app():
    flask_app = Flask(__name__)

    # Initializing MongoDB Connection
    flask_app.config['MONGODB_SETTINGS'] = {'host': config.MONGODB_CONNECTION_STRING}
    db.init_app(flask_app)

    # Initializing JWT Manager
    flask_app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    flask_app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
    flask_app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10)
    flask_app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1)
    jwt.init_app(flask_app)

    # CSRF
    flask_app.config['JWT_ACCESS_CSRF_COOKIE_NAME'] = config.JWT_ACCESS_CSRF_COOKIE_NAME
    flask_app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = config.JWT_ACCESS_CSRF_HEADER_NAME
    flask_app.config['JWT_REFRESH_CSRF_COOKIE_NAME'] = config.JWT_REFRESH_CSRF_COOKIE_NAME
    flask_app.config['JWT_REFRESH_CSRF_HEADER_NAME'] = config.JWT_REFRESH_CSRF_HEADER_NAME

    # Initializing Bcrypt module
    bcrypt = Bcrypt(flask_app)

    return flask_app
