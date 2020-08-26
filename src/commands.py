from flask.cli import FlaskGroup
from secrets import token_urlsafe

from src.app import create_app
from src.database import db
from src.blueprints.users.models import User

cli = FlaskGroup(create_app=create_app)
app = create_app()


@cli.command()
def drop_db():
    db.drop_all()
    db.session.commit()


@cli.command()
def seed_db():
    User.create(email='admin@example.com', password='admin', admin=True)