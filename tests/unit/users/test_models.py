"""Tests for the users blueprint models."""
from src.blueprints.users.models import User


class TestUser:
    """Tests for the User model."""

    def test_create_user(self, app):
        """Test the creation of a User object."""
        # GIVEN an application context
        # WHEN we try to create a user
        # THEN a user is created
        actual = User.create(email='test@test.com', password='test')
        expected = User.get_by_id(actual.id)
        assert actual == expected
    
    def test_user_password(self, user):
        """Test the set_password and check_password methods."""
        # GIVEN a user
        # WHEN the password is changed and checked
        # THEN the password is updated and the check works with tne new
        #   password
        assert user.check_password('user')
        user.set_password('new')
        assert user.password != 'new'
        assert not user.check_password('user')
        assert user.check_password('new')

    def test_update_user(self, user):
        """Test the update method for the User object."""
        # GIVEN a user
        # WHEN the user is updated
        # THEN the user is updated
        user.update(email='new@new.com', password='new')
        assert user.email == 'new@new.com'
        assert not user.password == 'new'
        assert user.check_password('new')