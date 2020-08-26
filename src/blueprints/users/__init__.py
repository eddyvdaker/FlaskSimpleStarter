from flask import Blueprint

bp = Blueprint('users', __name__)

from src.blueprints.users.routes import admin, auth, api
from src.blueprints.users import models