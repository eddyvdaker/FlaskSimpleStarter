import secrets
import os
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