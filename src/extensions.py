from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'users.login'

