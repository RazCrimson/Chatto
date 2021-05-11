"""
Config Module to read all the environment variables for the application configuration

Author: Raz Crimson
"""

from os import environ
from dotenv import load_dotenv

load_dotenv()

# MongoDB Credentials
MONGODB_DB = environ.get("MONGODB_DB", "")
MONGODB_HOST = environ.get("MONGODB_HOST", "localhost")
MONGODB_PORT = int(environ.get("MONGODB_PORT", 27017))
MONGODB_USERNAME = environ.get("MONGODB_USERNAME", "")
MONGODB_PASSWORD = environ.get("MONGODB_PASSWORD", "")

# App configuration
APP_HOST = environ.get("APP_HOST", "127.0.0.1")
APP_PORT = int(environ.get("APP_PORT", 5000))
APP_DEBUG = environ.get("APP_DEBUG", True)
