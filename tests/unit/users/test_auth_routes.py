"""Tests for the users blueprint auth routes."""
from tests.helpers.request_helpers import send_get, send_post
from tests.helpers.auth_helpers import login_user


class TestLogin:
    """Tests for the login route."""
    URL = '/users/login'

    def test_login_page(self, client):
        """Test the login page."""
        # GIVEN a test client
        # WHEN we browse to the login page
        # THEN the login page is loaded
        resp = send_get(client, self.URL)
        page = resp.data.decode()
        assert resp.status_code == 200
        assert '<h1>Login</h1>' in page
        assert 'email' in page
        assert 'password' in page
        assert 'remember' in page
        assert 'submit' in page

    def test_login(self, client, user):
        """Test the login page login form."""
        # GIVEN a user
        # WHEN the user logs in on the login page
        # THEN the user is logged in and redirected to the index page
        data={'email': user.email, 'password': user.plain_pass}
        resp = send_post(client, self.URL, data=data)
        assert resp.status_code == 200
        assert 'Logout' in resp.data.decode()

    def test_missing_email(self, client, user):
        """Test the login page form with missing email."""
        # GIVEN a user
        # WHEN the users tries to log in without an email
        # THEN an error message is shown
        data = {'password': user.plain_pass}
        resp = send_post(client, self.URL, data=data)
        assert 'required' in resp.data.decode()

    def test_missing_password(self, client, user):
        """Test the login page form with missing password."""
        # GIVEN a user
        # WHEN the users tries to log in without a password
        # THEN an error message is shown
        data = {'email': user.email}
        resp = send_post(client, self.URL, data=data)
        assert 'required' in resp.data.decode()

    def test_wrong_password(self, client, user):
        """Test the login page form with wrong password."""
        # GIVEN a user
        # WHEN the user tries to log in with the wrong password
        # THEN an error message is shown
        data = {'email': user.email, 'password': 'wrong-pass'}
        resp = send_post(client, self.URL, data=data)
        assert 'Wrong' in resp.data.decode()



class TestLogout:
    """Tests for the logout route."""
    URL = '/users/logout'

    def test_logout(self, client, user):
        """Test the logout route."""
        # GIVEN a user
        # WHEN the user logs in and then out
        # THEN the user is logged out
        login_user(client, user)
        resp = send_get(client, self.URL, follow_redirects=True)
        assert resp.status_code == 200
        assert not 'Logout' in resp.data.decode()