"""Authentication routes for the users blueprint."""
from flask import flash, redirect, url_for, render_template, request
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse

from src.blueprints.users import bp
from src.blueprints.users.forms import LoginForm
from src.blueprints.users.models import User


@bp.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Wrong username or password')
            return redirect(url_for('users.login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('form.html', form=form, title='Login')


@bp.route('/users/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))