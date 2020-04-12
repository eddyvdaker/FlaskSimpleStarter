from flask import render_template

from src.blueprints.main import bp
from src.blueprints.users.utils import admin_required


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/admin')
@admin_required
def admin():
    return render_template('admin.html')
