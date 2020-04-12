"""Generic forms that can be used throughout the application."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class ConfirmForm(FlaskForm):
    confirm = BooleanField('Confirm', validators=[DataRequired()])
    submit = SubmitField('Submit')