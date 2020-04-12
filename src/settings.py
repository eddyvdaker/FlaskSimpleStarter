import secrets
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe()
TESTING = os.environ.get('TESTING') or False
DEV = os.environ.get('DEVELOPMENT') or False