from src.extensions import db

# Alias common SQLAlchemy elements
Column = db.Column
relationship = db.relationship
String = db.String
Text = db.Text
Integer = db.Integer
DateTime = db.DateTime
Boolean = db.Boolean
ForeignKey = db.ForeignKey
Table = db.Table
backref = db.backref


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
            return cls.query.get(int(record_id))
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
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Model(db.Model, CRUDMixin):
    """Base model class."""
    __abstract__ = True


def rollback_db():
    """Helper function for executing a DB rollback."""
    db.session.rollback()
    db.session.commit()
