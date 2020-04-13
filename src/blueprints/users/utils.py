"""Utilities provided by the users blueprint."""
from flask import abort, redirect, url_for
from flask_login import current_user
from functools import wraps


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kw):
        if not current_user.is_anonymous:
            if current_user.admin:
                return func(*args, **kw)
        else:
            return redirect(url_for('users.login'))
        abort(403)
    return wrapper