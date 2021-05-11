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
