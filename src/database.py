from types import SimpleNamespace
from flask import has_app_context
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from src.settings import SQLALCHEMY_DATABASE_URI

metadata = MetaData()
Base = declarative_base(metadata=metadata)
# The SQLAlchemy extension is created here instead of in extensions.py
# because it needs information from the database.py file. However, the
# database.py file also requires the db object. This would lead to a
# circular import if the db object was created in the extensions.py
# file. The db object is imported in the extensions.py file to provide
# a unified method of accessing the Flask extensions.
db = SQLAlchemy(metadata=metadata)
engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(engine)
plain_db = SimpleNamespace()
plain_db.session = session


class CRUDMixin(object):
    """Mixin that adds convenient methods for CRUD."""

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float))
            ),
        ):
            return cls.query().get(int(record_id))
        return None

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()
    
    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def save(self):
        if not has_app_context():
            db.session = session
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        if not has_app_context():
            db.session = session
        db.session.delete(self)
        db.session.commit()


class Model(Base, CRUDMixin):
    """Base model class."""
    __abstract__ = True

    def __init__(self, **kwargs):
        self.update(**kwargs)

    def __repr__(self):
        if hasattr(self, 'id'):
            return f'<{self.__class__.__name__} {self.id}>'
        return super().__repr__()

    @classmethod
    def query(cls):
        if not has_app_context():
            db.session = session
        return db.session.query(cls)


def rollback_db():
    """Helper function for executing a DB rollback."""
    db.session.rollback()
    db.session.commit()
