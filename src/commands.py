from flask.cli import FlaskGroup
from secrets import token_urlsafe

from src.app import create_app
from src.database import db
from src.blueprints.users.models import User

cli = FlaskGroup(create_app=create_app)
app = create_app()


@cli.command()
def recreate_db():
    """Drop the current database and recreate it."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    password = token_urlsafe(12)
    User.create(email='admin@example.com', password=password, admin=True)
    print(password)