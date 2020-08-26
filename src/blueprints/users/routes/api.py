"""API routes for the users blueprint."""
from flask import current_app

from src.blueprints.users import bp
from src.blueprints.users.api_auth import basic_auth, token_auth


@bp.route('/api/v1.0/request-key')
@basic_auth.login_required
def request_key():
    key = basic_auth.current_user().get_key(
        current_app.config['EXPIRATION_TIME'])
    return key


@bp.route('/api/v1.0/test-auth')
@token_auth.login_required
def test_token_auth():
    return {'status': 'success'}
