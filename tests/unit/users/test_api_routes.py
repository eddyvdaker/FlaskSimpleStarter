"""Tests for the users blueprints api authentication routes."""
from requests.auth import _basic_auth_str

from tests.helpers.request_helpers import send_get


class TestAPIAuth:
    """Tests for the API Auth."""

    def test_api_auth(self, client, user):
        """Test the request key route and authentication route."""
        # GIVEN a user
        # WHEN the user requests a key
        # THEN a key is returned and this key can be used to
        #       authenticate with the application
        headers = {'Authorization': _basic_auth_str(
            user.email, user.plain_pass)}
        resp = send_get(client, "/api/v1.0/request-key", headers=headers)
        exepected_status = 200
        assert resp.status_code == exepected_status
        assert resp.is_json
        data = resp.get_json()
        assert 'key' in data

        resp = send_get(client, '/api/v1.0/test-auth', key=data['key'])
        expected_json = {'status': 'success'}
        assert resp.status_code == exepected_status
        assert resp.is_json
        data = resp.get_json()
        assert data == expected_json

    def test_api_auth_wrong_user(self, client, user):
        """Test the request a key route with the wrong username."""
        # GIVEN a user
        # WHEN the user requests a key with the wrong username
        # THEN an error is returned
        headers = {'Authorization': _basic_auth_str(
            'wrong@user.com', user.plain_pass)}
        resp = send_get(client, "/api/v1.0/request-key", headers=headers)
        exepected_status = 401
        assert resp.status_code == exepected_status
    
    def test_api_auth_wrong_pass(self, client, user):
        """Test the request a key route with the wrong password."""
        # GIVEN a user
        # WHEN the user requests a key with the wrong password
        # THEN an 401 error is returned
        headers = {'Authorization': _basic_auth_str(
            user.email, 'wrong')}
        resp = send_get(client, "/api/v1.0/request-key", headers=headers)
        exepected_status = 401
        assert resp.status_code == exepected_status

    def test_api_auth_wrong_key(self, client, user, api_key):
        """Test the auth test route with the wrong key."""
        # GIVEN a user
        # WHEN the user visits the auth test route with the wrong key
        # THEN a 401 error is returned
        headers = {'Authorization': 'Bearer SOMEWRONGKEY'}
        resp = send_get(client, '/api/v1.0/test-auth', headers=headers)
        expected_status = 401
        assert resp.status_code == expected_status