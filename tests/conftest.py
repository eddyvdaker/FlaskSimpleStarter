import pytest

from src.app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture
def client(app):
    return app.test_client()
