from flask import Flask

from src.blueprints import main, users
from src.errors import bp as errors_bp
from src.extensions import bootstrap, db, login, migrate



def create_app(config_object: str = 'src.settings') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)

    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)


def register_blueprints(app):
    app.register_blueprint(errors_bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(users.bp)


def register_shellcontext(app):
    def shell_context():
        return {
            'db': db,
            'User': users.models.User,
            'ApiKey': users.models.ApiKey
        }
    app.shell_context_processor(shell_context)
