"""Admin routes for the users blueprint."""
from flask import flash, redirect, url_for, render_template, abort
from sqlalchemy.exc import IntegrityError

from src.database import rollback_db
from src.forms import ConfirmForm
from src.blueprints.users import bp
from src.blueprints.users.forms import UserForm, PasswordForm, NewUserForm
from src.blueprints.users.models import User
from src.blueprints.users.utils import admin_required


@bp.route('/admin/users')
@admin_required
def overview_users():
    users = User.query().all()
    return render_template('users/admin/overview.html', users=users)


@bp.route('/admin/users/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        abort(404)
    form = UserForm()
    if form.validate_on_submit():
        try:
            user.update(email=form.email.data, admin=form.admin.data)
            flash('User updated')
            return redirect(url_for('users.overview_users'))
        except IntegrityError:
            rollback_db()
            flash('Email already in use')
    else:
        form.email.data = user.email
        form.admin.data = user.admin
    return render_template('form.html', form=form,
        title=f'Edit User: {user.id} ({user.email})')


@bp.route('/admin/users/<int:user_id>/password', methods=['GET', 'POST'])
@admin_required
def reset_password(user_id):
    user = User.get_by_id(user_id)
    if not user:
        abort(404)
    form = PasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password_1.data)
        flash('Password reset')
        return redirect(url_for('users.overview_users'))
    return render_template('form.html', form=form,
        title=f'Reset Password: {user.id} ({user.email})')
 

@bp.route('/admin/users/<int:user_id>/delete', methods=['GET', 'POST'])
@admin_required
def delete_user(user_id):
    user = User.get_by_id(user_id)
    if not user:
        abort(404)
    form = ConfirmForm()
    if form.validate_on_submit() and form.confirm.data:
        user.delete()
        flash('User deleted')
        return redirect(url_for('users.overview_users'))
    return render_template('form.html', form=form,
        title=f'Delete User: {user.id} ({user.email})',
        extra_text=f'Are you sure you want to delete user {user.id} '\
            f'({user.email}), this cannot be undone.')
    

@bp.route('/admin/users/new', methods=['GET', 'POST'])
@admin_required
def new_user():
    form = NewUserForm()
    if form.validate_on_submit():
        try:
            user = User.create(
                email=form.email.data,
                password=form.password_1.data,
                admin=form.admin.data
            )
            flash('New user created')
            return redirect(url_for('users.overview_users'))
        except IntegrityError:
            rollback_db()
            flash('Email already in use')
    return render_template('form.html', form=form, title='New User')