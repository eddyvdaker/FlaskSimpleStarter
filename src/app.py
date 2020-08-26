import os
import logging
from flask import Flask
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler, SMTPHandler

from flask.wrappers import Request

from src.blueprints import main, users
from src.errors import bp as errors_bp
from src.extensions import bootstrap, db, login, migrate
from src.utils import RequestFormatter


def create_app(config_object: str = 'src.settings') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    if not app.config['TESTING']:
        register_logging(app)
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


def register_logging(app):
    formatter = RequestFormatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d] - [from %(remote_addr)s to %(url)s]')

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(f'logs/{app.config["APP_NAME"]}.log',
        maxBytes=app.config['LOGGING_SIZE'],
        backupCount=app.config['LOGGING_BACKUP_COUNT'])
    file_handler.setFormatter(formatter)
    file_handler.setLevel(app.config['LOGGING_LEVEL'])
    app.logger.addHandler(file_handler)

    logging_email = app.config.get('LOGGING_EMAIL')
    mail_server = app.config.get('MAIL_SERVER')
    mail_port = app.config.get('MAIL_PORT')
    if logging_email and mail_server and mail_port:
        auth = None
        if app.config.get('MAIL_USERNAME') or app.config.get('MAIL_PASSWORD'):
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config.get('MAIL_USE_TSL'):
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(mail_server, mail_port),
            fromaddr=f'no-reply@{mail_server}',
            toaddrs=[logging_email],
            subject=f'{app.config["APP_NAME"]} Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
