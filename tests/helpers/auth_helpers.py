"""Helpers for authentication."""
from tests.helpers.request_helpers import send_post


def login_user(client, user):
    """Login the given user."""
    data={'email': user.email, 'password': user.plain_pass}
    return send_post(client, '/users/login', data=data, follow_redirects=True)
