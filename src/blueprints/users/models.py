"""Models for the users blueprint."""
from base64 import b64encode
from datetime import datetime, timedelta
from flask_login import UserMixin
from typing import Dict
from secrets import token_urlsafe
from werkzeug.security import generate_password_hash, check_password_hash

from src.database import ForeignKey, Model, Column, Integer, String, Boolean, \
    DateTime, relationship
from src.extensions import login


class User(Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(64), index=True, nullable=False, unique=True)
    password = Column(String(254))
    admin = Column(Boolean, default=False)

    api_keys = relationship('ApiKey', lazy='dynamic', backref='key_user')
    
    @classmethod
    def create(cls, **kwargs):
        """Override of the CRUDMixin create method to handle the
        passwords correctly.
        """
        user = cls(**kwargs)
        if 'password' in kwargs:
            user.set_password(kwargs['password'])
        return user.save()

    def update(self, **kwargs):
        """Override of the CRUDMixin update method to handle the
        passwords correctly.
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if 'password' in kwargs:
            self.set_password(kwargs['password'])
        return self.save()

    def set_password(self, password: str):
        """Set password field to a hash + salt value of the given 
        password.
        :param password: the password to set for this user.
        """
        if password:
            self.password = generate_password_hash(password)
            self.save()

    def check_password(self, password: str) -> bool:
        """Check if the given password is correct.
        :param password: the password to check.
        :return: True if password is correct, False if it is not.
        """
        if password and self.password:
            return check_password_hash(self.password, password)
        return False

    def get_key(self, expires_in) -> Dict:
        """Request a token for this user.
        :param expires_in: Time the key is valid after creation or last use
            (in seconds)
        :return: A dictionary with API key information
        """
        key = ApiKey.create(user_id=self.id)
        key.update(expiration=key.created + timedelta(seconds=expires_in))
        return key.to_dict()

    def revoke_key(self, key):
        """Revoke an API key.
        :param key: the key to revoke
        """
        api_key = self.api_keys.filter_by(key=key).first()
        if api_key and api_key in self.api_keys.all():
            api_key.delete()

    @staticmethod
    def check_key(key) -> bool:
        """Check an API key.   
        :param key: The key to check
        :return: Self if the API key is valid, nothing otherwise    
        """
        api_key = ApiKey.query.filter_by(key=key).first()
        if api_key:
            if datetime.utcnow() < api_key.expiration:
                return api_key
    
    def to_dict(self) -> Dict:
        return {'id': self.id, 'email': self.email,  'admin': self.admin}


class ApiKey(Model):
    __tablename__ = 'api_key'

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    created = Column(DateTime, default=datetime.utcnow())
    last_used = Column(DateTime)
    expiration = Column(DateTime)

    user_id = Column(Integer, ForeignKey('user.id'))

    @classmethod
    def create(cls, **kwargs):
        """Override of the CRUDMixin create method to handle duplicate key
        checking"""
        key = token_urlsafe(32)
        encoded_key = key.encode('utf-8')
        b64_key = b64encode(encoded_key)
        b64_key_str = b64_key.decode('utf-8')
        while ApiKey.query.filter_by(key=b64_key_str).first():
            encoded_key = key.encode('utf-8')
            b64_key = b64encode(encoded_key)
            b64_key_str = b64_key.decode('utf-8')
            key = token_urlsafe(32)
        key = cls(key=b64_key_str, **kwargs)
        return key.save()

    @classmethod
    def get_by_key(cls, key):
        """Request an API key object from a key."""
        return cls.query.filter_by(key=key).first()

    def update_key_expiration(self, expires_in):
        """Update the expiration time.
        :param expires_in: expiration time in seconds
        """
        if self.last_used:
            self.update(expiration=self.last_used +
                timedelta(seconds=expires_in))
        else:
            self.update(expiration=self.created +
                timedelta(seconds=expires_in))

    def to_dict(self) -> Dict:
        api_dict = {
            'id': self.id,
            'key': self.key,
            'created': self.created.isoformat(),
            'last_used': None,
            'expiration': self.expiration.isoformat(),
            'user': self.user_id
        }
        if self.last_used:
            api_dict['last_used'] = self.last_used.isoformat()
        return api_dict


@login.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)