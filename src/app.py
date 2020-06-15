from flask import Flask

from src.blueprints import main
from src.errors import bp as errors_bp
from src.extensions import bootstrap


def create_app(config_object: str = 'src.settings') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)

    return app


def register_extensions(app):
    bootstrap.init_app(app)


def register_blueprints(app):
    app.register_blueprint(errors_bp)
    app.register_blueprint(main.bp)


def register_shellcontext(app):
    def shell_context():
        return {

        }
    app.shell_context_processor(shell_context)
