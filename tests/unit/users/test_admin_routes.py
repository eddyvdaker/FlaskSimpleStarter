""" Tests for the users blueprint admin routes."""
from src.blueprints.users.models import User

from tests.helpers.request_helpers import send_get, send_post
from tests.helpers.auth_helpers import login_user


class TestUserOverview:
    """Tests for the user overview route."""
    URL = '/admin/users'

    def test_user_overview(self, client, admin):
        """Test the user overview page."""
        # GIVEN an admin user
        # WHEN the admin user visists the user overview page
        # THEN the user overview page is shown with admin buttons
        login_user(client, admin)
        resp = send_get(client, self.URL)
        assert resp.status_code == 200
        data = resp.data.decode()
        assert 'Add User' in data
        assert admin.email in data
        assert 'Reset Password' in data
        assert 'Edit' in data
        assert 'Delete' in data

    def test_user_overview_non_admin(self, client, user):
        """Test the user overview page with a non-admin user."""
        # GIVEN a normal user
        # WHEN the user visists the user overview page
        # THEN a 403 error is thrown
        login_user(client, user)
        resp = send_get(client, self.URL)
        assert resp.status_code == 403
    
    def test_user_overview_not_logged_in(self, client):
        """Test the user overview page without logging in."""
        # GIVEN a user that is not logged in
        # WHEN the user visits the user overview page
        # THEN the user is redirected to the login page
        resp = send_get(client, self.URL, follow_redirects=True)
        assert '<h1>Login</h1>' in resp.data.decode()


class TestEditUser:
    """Tests for the edit user route."""
    URL = '/admin/users'

    def test_edit_user(self, client, admin):
        """Test the edit user form."""
        # GIVEN an admin user
        # WHEN the user visists the edit user page
        # THEN the user gets the edit user page
        login_user(client, admin)
        resp = send_get(client, f'{self.URL}/{admin.id}')
        assert resp.status_code == 200
        data = resp.data.decode()
        assert 'Edit User:' in data
        assert 'Email' in data
        assert 'Admin' in data

    def test_edit_user_non_admin(self, client, user):
        """Test the edit user form with a non-admin user."""
        # GIVEN a non-admin user
        # WHEN the user visists the edit user page
        # THEN a 403 error is thrown
        login_user(client, user)
        resp = send_get(client, f'{self.URL}/{user.id}')
        assert resp.status_code == 403

    def test_edit_user_no_login(self, client, admin):
        """Test the edit user form without logging in."""
        # GIVEN a user that is not logged in
        # WHEN the user visists the edit user page
        # THEN the user is redirected to the login page
        resp = send_get(client, f'{self.URL}/{admin.id}',
            follow_redirects=True)
        assert '<h1>Login</h1>' in resp.data.decode()

    def test_post_user_edit(self, client, admin):
        """Test the sending of data trough the form."""
        # GIVEN an admin user
        # WHEN the users submits the form
        # THEN the user is changed
        login_user(client, admin)
        old_email = admin.email
        resp = send_post(client, f'{self.URL}/{admin.id}',
            data={'email': 'new@email.com', 'admin': True})
        assert resp.status_code == 200
        data = resp.data.decode()
        assert 'Admin: User Overview' in data
        assert 'new@email.com' in data
        assert not old_email in data
        new_admin = User.get_by_id(admin.id)
        assert new_admin.email == 'new@email.com'
        
    def test_post_edit_without_email(self, client, admin):
        """Test the sending of data with missing keys."""
        # GIVEN an admin user
        # WHEN the user submits the form without email
        # THEN an error message is shown
        login_user(client, admin)
        resp = send_post(client, f'{self.URL}/{admin.id}', 
            data={'admin': True})
        data = resp.data.decode()
        assert 'required' in data
        assert 'Edit User:' in data

    def test_post_edit_wrong_email_format(self, client, admin):
        """Test the sending of data with a wrongly formatted email
        address.
        """
        # GIVEN an admin user
        # WHEN the user submits the form with a wrongly formatted email
        #   address
        # THEN an error message is shown
        login_user(client, admin)
        resp = send_post(client, f'{self.URL}/{admin.id}',
            data={'email': 'new', 'admin': True})
        assert 'Invalid email address' in resp.data.decode()

    def test_non_existing_user(self, client, admin):
        """Test the edit user route with a non-existing user."""
        # GIVEN an admin user
        # WHEN the user tries to edit a non-existing user
        # THEN a 404 error is returned
        login_user(client, admin)
        resp = send_post(client, f'{self.URL}/50',
            data={'email': 'email@email.com', 'admin': False})
        assert resp.status_code == 404

    def test_duplicate_email(self, client, admin, user):
        """Test the editing user with duplicate email."""
        # GIVEN an admin user and another user
        # WHEN the admin edits a user with a duplicate email
        # THEN an error message is shown
        login_user(client, admin)
        resp = send_post(client, f'{self.URL}/{user.id}',
            data={'email': admin.email, 'admin': False})
        assert 'already in use' in resp.data.decode()



class TestResetPassword:
    """Tests for the reset password route."""
    URL = '/admin/users'

    def test_reset_password(self, client, admin):
        """Test the reset password page."""
        # GIVEN an admin user
        # WHEN the user visists the reset password page
        # THEN the reset password page is shown
        login_user(client, admin)
        resp = send_get(client, f'{self.URL}/{admin.id}/password')
        assert resp.status_code == 200
        data = resp.data.decode()
        assert 'Reset Password:' in data
        assert 'Repeat Password' in data

    def test_reset_password_non_admin(self, client, user):
        """Test the reset password page with a user that is not an
        admin user.
        """
        # GIVEN a non-admin user
        # WHEN the user visists the reset password page
        # THEN a 403 error is thrown
        login_user(client, user)
        resp = send_get(client, f'{self.URL}/{user.id}/password')
        assert resp.status_code == 403

    def test_reset_password_without_login(self, client, admin):
        """Test the reset password page without logging in."""
        # GIVEN a user that is not logged in
        # WHEN the user visists the reset password page
        # THEN the user is redirected to the login page
        resp = send_get(client, f'{self.URL}/{admin.id}/password',
            follow_redirects=True)
        assert '<h1>Login</h1>' in resp.data.decode()
    
    def test_reset_password_form(self, client, admin):
        """Test the reset password form."""
        # GIVEN an admin user
        # WHEN the user sends data through the form
        # THEN the password is reset
        login_user(client, admin)
        resp = send_post(client, f'{self.URL}/{admin.id}/password',
            data={'password_1': 'new', 'password_2': 'new'})
        assert resp.status_code == 200
        data = resp.data.decode()
        assert 'Password reset' in data
        assert 'Overview' in data
        assert admin.check_password('new')
        assert not admin.check_password(admin.plain_pass)

    def test_reset_password_form_not_equal(self, client, admin):
        """Test the reset password form when the passwords are not
        equal.
        """
        # GIVEN an admin user
        # WHEN the user sends data through the form, but the passwords
        #   are different
        # THEN an error message is shown
        login_user(client, admin)
        resp = send_post(client, f'{self.URL}/{admin.id}/password',
            data={'password_1': 'pass1', 'password_2': 'pass2'})
        assert 'must be equal' in resp.data.decode()

    def test_reset_password_form_missing_fields(self, client, admin):
        """Test the reset password form when a field is missing."""
        # GIVEN an admin user
        # WHEN the user sends data through the form, but a field is
        #   missing
        # THEN an error message is shown
        login_user(client, admin)
        resp = send_post(client, f'{self.URL}/{admin.id}/password',
            data={'password_2': 'new'})
        assert 'required' in resp.data.decode()


class TestDeleteUser:
    """Tests for the delete user route."""
    URL = '/admin/users'

    def test_delete_user_page(self, client, admin):
        """Test the delete user page."""
        # GIVEN an admin user
        # WHEN the user visits the delete user page
        # THEN the delete users page is shown
        login_user(client, admin)
        resp = send_get(client, f'{self.URL}/{admin.id}/delete')
        assert resp.status_code == 200
        data = resp.data.decode()
        assert 'Delete User:' in data
        assert 'Confirm' in data
        assert admin.email in data

    def test_delete_user_page_non_admin(self, client, user):
        """Test the delete user page with a non-admin user."""
        # GIVEN a non-admin user
        # WHEN the user visists the delete user page
        # THEN a 403 error is shown
        login_user(client, user)
        resp = send_get(client, f'{self.URL}/{user.id}/delete')
        assert resp.status_code == 403

    def test_delete_user_page_without_login(self, client, admin):
        """Test the delete user page without login."""
        # GIVEN a user that is not logged in
        # WHEN the user visists the delete user page
        # THEN the user is redirected to the login page
        resp = send_get(client, f'{self.URL}/{admin.id}/delete',
            follow_redirects=True)
        assert '<h1>Login</h1>' in resp.data.decode()

    def test_delete_user(self, client, admin, user):
        """Test the delete user form."""
        # GIVEN an admin user and another user
        # WHEN the admin deletes the other user
        # THEN the other user is deleted
        login_user(client, admin)
        resp = send_post(client, f'{self.URL}/{user.id}/delete',
            data={'confirm': True})
        data = resp.data.decode()
        assert 'Overview' in data
        assert admin.email in data
        assert not user.email in data
        assert not User.get_by_id(user.id)

    def test_delete_user_not_confirmed(self, client, admin, user):
        """Test the delete user form when confirm is not selected."""
        # GIVEN an admin user and another user
        # WHEN the admin deletes the user but does not confirm
        # THEN the user is not deleted and an error message is shown
        login_user(client, admin)
        resp = send_post(client, f'{self.URL}/{user.id}/delete', data={})
        assert User.get_by_id(user.id)
 

class TestNewUser:
    """Tests for the new users route."""
    URL = '/admin/users/new'

    def test_new_user_page(self, client, admin):
        """Test the new user page."""
        # GIVEN an admin user
        # WHEN the user visists the new user page
        # THEN the new user page is shown
        login_user(client, admin)
        resp = send_get(client, self.URL)
        assert resp.status_code == 200
        data = resp.data.decode()
        assert 'New User' in data
        assert 'Email' in data
        assert 'Password' in data
        assert 'Repeat Password' in data
        assert 'Admin' in data
        assert 'Create' in data

    def test_new_user_page_non_admin(self, client, user):
        """Test the new user page with a non-admin user."""
        # GIVEN a non-admin user
        # WHEN the user visists the new user page
        # THEN a 403 error is shown
        login_user(client, user)
        resp = send_get(client, self.URL)
        assert resp.status_code == 403

    def test_new_user_without_login(self, client):
        """Test the new user page without login."""
        # GIVEN a user without login
        # WHEN the user visists the new user page
        # THEN the user is redirect to the login page
        resp = send_get(client, self.URL, follow_redirects=True)
        assert '<h1>Login</h1>' in resp.data.decode()

    def test_new_user(self, client, admin):
        """Test the new user form."""
        # GIVEN an admin user
        # WHEN the admin creates a new user through the form
        # THEN the new user is created
        login_user(client, admin)
        resp = send_post(client, self.URL, data={'email': 'user@user.com', 
            'password_1': 'user', 'password_2': 'user', 'admin': True})
        assert resp.status_code == 200
        data = resp.data.decode()
        assert 'New user created' in data
        assert 'user@user.com' in data

    def test_new_user_missing_field(self, client, admin):
        """Test the new user form with missing fields."""
        # GIVEN an admin user
        # WHEN the admin creates a new user through the form with
        #   missing fields
        # THEN an error message is shown
        login_user(client, admin)
        resp = send_post(client, self.URL, data={'password_1': 'user',
            'password_2': 'user', 'admin': True})
        assert 'required' in resp.data.decode()

    def test_new_user_different_passwords(self, client, admin):
        """Test the new user form with non-matching passwords."""
        # GIVEN an admin user
        # WHEN the admin creates a new user through the form and the
        #   passwords don't match
        # THEN an error message is shown
        login_user(client, admin)
        resp = send_post(client, self.URL, data={'email': 'user@user.com',
            'password_1': 'pass1', 'password_2': 'pass2', 'admin': True})
        assert 'equal' in resp.data.decode()

    def test_new_user_duplicate_email(self, client, admin):
        """Test the new user form with duplicate email."""
        # GIVEN an admin user
        # WHEN the admin creates a new user through the form with a
        #   duplicate email
        # THEN an error message is shown
        login_user(client, admin)
        resp = send_post(client, self.URL, data={'email': admin.email,
            'password_1': 'pass', 'password_2': 'pass', 'admin': True})
        assert 'already in use' in resp.data.decode()