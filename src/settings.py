import secrets
import os
import logging
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

APP_NAME = os.environ.get('APP_NAME') or 'APP_NAME'
SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe()
TESTING = os.environ.get('TESTING') or False
DEV = os.environ.get('DEVELOPMENT') or False

## DB Settings
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, '../data/app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

## Auth Settings
EXPIRATION_TIME = os.environ.get('EXPIRATION_TIME') or 2629800

## Logging Settings
logging_level = os.environ.get("LOGGING_LEVEL")
if logging_level == 'DEBUG':
    LOGGING_LEVEL = logging.DEBUG
elif logging_level == 'INFO':
    LOGGING_LEVEL = logging.INFO
elif logging_level == 'WARNING':
    LOGGING_LEVEL = logging.WARNING
elif logging_level == 'ERROR':
    LOGGING_LEVEL =  logging.ERROR
elif logging_level == 'CRITICAL':
    LOGGING_LEVEL = logging.CRITICAL
else:
    LOGGING_LEVEL = logging.WARNING
LOGGING_BACKUP_COUNT = os.environ.get('LOGGING_BACKUP_COUNT') or 10
LOGGING_SIZE = os.environ.get('LOGGING_SIZE') or 10240
LOGGING_EMAIL = os.environ.get("LOGGING_EMAIL")

## Email Settings
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')