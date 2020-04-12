"""    Models for the users blueprint."""
from flask_login import UserMixin
from typing import Dict
from werkzeug.security import generate_password_hash, check_password_hash

from src.database import Model, Column, Integer, String, Boolean
from src.extensions import login


class User(Model, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    email = Column(String(64), index=True, nullable=False, unique=True)
    password = Column(String(254))
    admin = Column(Boolean, default=False)
    
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
    
    def to_dict(self) -> Dict:
        return {'id': self.id, 'email': self.email,  'admin': self.admin}


@login.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)