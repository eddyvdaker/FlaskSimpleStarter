"""Fixtures for users."""
import pytest

from src.blueprints.users.models import User, ApiKey


@pytest.fixture
def user(app):
    """Create a single user."""
    user = User.create(email='user@user.com', password='user')
    user.plain_pass = 'user'
    return user


@pytest.fixture
def admin(app):
    """Create an admin user."""
    user = User.create(email='admin@admin.com', password='admin', admin=True)
    user.plain_pass = 'admin'
    return user


@pytest.fixture
def users(admin):
    """Create a number of users."""
    users = [admin]
    for i in range(4):
        user = User.create(email=f'user{i+1}@user.com', password='user')
        user.plain_pass = 'user'
        users.append(user)
    return users


@pytest.fixture
def api_key(user):
    """Create an API key."""
    key = user.get_key(100)
    return ApiKey.get_by_id(key['id'])