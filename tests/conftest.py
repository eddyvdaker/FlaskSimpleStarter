import pytest

from src.app import create_app
from src.extensions import db
from tests._fixtures import *


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['WTF_CSRF_ENABLED'] = False
    
    ctx = app.app_context()
    ctx.push()

    db.create_all()
    db.session.commit()

    yield app

    db.drop_all()
    ctx.pop()


@pytest.fixture
def client(app):
    return app.test_client()
