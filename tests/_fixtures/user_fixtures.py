"""Fixtures for users."""
import pytest

from src.blueprints.users.models import User


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