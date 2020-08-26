"""Tests for the users blueprint models."""
from src.blueprints.users.models import User, ApiKey


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

    def test_get_key(self, user):
        """Test the get_user method for the User object."""
        # GIVEN a user
        # WHEN we request a key for that user
        # THEN a key is returned
        actual = user.get_key(100)
        assert 'id' in actual
        assert 'key' in actual
        assert 'created' in actual
        assert 'last_used' in actual
        assert 'expiration' in actual
        assert 'user' in actual
        assert ApiKey.get_by_id(actual['id'])

    def test_revoke_key(self, user, api_key):
        """Test the revoke key method for a user."""
        # GIVEN a user and a key
        # WHEN we revoke the key for the user
        # THEN the key is deleted
        user.revoke_key(api_key.key)
        assert not ApiKey.get_by_id(api_key.id)

    def test_revoke_key_other_user(self, users, api_key):
        """Test the revoke key method on a user with a key that does
        not belong to that user.
        """
        # GIVEN a user and a key that does not belong to that user
        # WHEN we revoke the key on the user
        # THEN nothing happens
        users[-1].revoke_key(api_key.key)
        assert ApiKey.get_by_id(api_key.id)

    def test_check_key(self, api_key):
        """Test the check key method."""
        # GIVEN a key
        # WHEN we check the key
        # THEN true is returned
        assert User.check_key(api_key.key)

    def test_check_wrong_key(self, app):
        """Test the check key method with a wrong key."""
        # GIVEN a wrong key
        # WHEN we check the key
        # THEN false is returned
        assert not User.check_key("abcdefg1234567")

    def test_check_expired_key(self, api_key):
        """Test the check key method for an expired key."""
        # GIVEN a expired key
        # WHEN we check the key
        # THEN false is returned
        api_key.update_key_expiration(-5)
        assert not User.check_key(api_key.key)


class TestApiKey:
    """Tests for the API Key model."""

    def test_create(self, user):
        """Test the creation of an key object."""
        # GIVEN a user
        # WHEN we create a key object
        # THEN a key object is created
        ApiKey(user_id=user.id)
    
    def test_get_by_key(self, api_key):
        """Test the get_by_key method."""
        # GIVEN an Api Key
        # WHEN we search for the key by the key value
        # THEN we get the key object
        assert ApiKey.get_by_key(api_key.key) == api_key

    def test_get_by_key_with_wrong_key(self, app):
        """Test the get_by_key method with a wrong key."""
        # GIVEN an non-existing API key
        # WHEN we search for the key by the key value
        # THEN nothing is returned
        assert not ApiKey.get_by_id('abcdefg1234567')

    def test_update_key_expiration(self, api_key):
        """Test the update_key_expiration method for a key."""
        # GIVEN an API key
        # WHEN we update the key expiration
        # THEN the key expiration is updated
        api_key.update_key_expiration(200)
