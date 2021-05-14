"""
Config Module to read all the environment variables for the application configuration

Author: Raz Crimson
"""

from os import environ
from dotenv import load_dotenv

load_dotenv()

# MongoDB Credentials
MONGODB_CONNECTION_STRING = environ.get("MONGODB_CONNECTION_STRING", "")

# App configuration
APP_HOST = environ.get("APP_HOST", "127.0.0.1")
APP_PORT = int(environ.get("APP_PORT", 5000))
APP_DEBUG = environ.get("APP_DEBUG", True)

# JWT Secret
JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", "")

# CSRF
JWT_ACCESS_CSRF_COOKIE_NAME = environ.get("JWT_ACCESS_CSRF_COOKIE_NAME")
JWT_ACCESS_CSRF_HEADER_NAME = environ.get("JWT_ACCESS_CSRF_HEADER_NAME")
JWT_REFRESH_CSRF_COOKIE_NAME = environ.get("JWT_REFRESH_CSRF_COOKIE_NAME")
JWT_REFRESH_CSRF_HEADER_NAME = environ.get("JWT_REFRESH_CSRF_HEADER_NAME")
