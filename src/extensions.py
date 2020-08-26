from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_login import LoginManager

from src.database import db

migrate = Migrate()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'users.login'

