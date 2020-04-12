from flask import Blueprint

bp = Blueprint('main', __name__)

from src.blueprints.main import routes
