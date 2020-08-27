"""This script is an example for how to work with the database models
in an external script.
"""
from random import randint
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src import settings
from src.blueprints.users.models import User
from src.database import metadata

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
session = Session(engine)
print(User.query().filter_by(email='admin@example.com').first())
print(User.create(email=f'test{randint(0, 5000)}@t.com', password='test'))