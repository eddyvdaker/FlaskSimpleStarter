"""Helpers for authenitcating API."""
from logging import error
from flask import current_app
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from src.blueprints.users.models import User
from src.errors import error_response

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')


@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user


@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)


@token_auth.verify_token
def verify_token(token):
    key = User.check_key(token) if token else None
    if key:
        key.update_key_expiration(current_app.config['EXPIRATION_TIME'])
        return key.key_user


@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)
