"""Forms for the users module."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, email, equal_to


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), email()])
    admin = BooleanField('Admin')
    submit = SubmitField('Save')


class PasswordForm(FlaskForm):
    password_1 = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Repeat Password',
        validators=[equal_to('password_1')])
    submit = SubmitField('Save')


class NewUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), email()])
    password_1 = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Repeat Password',
        validators=[equal_to('password_1')])
    admin = BooleanField('Admin')
    submit = SubmitField('Create')