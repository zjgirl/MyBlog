from flask import Blueprint
from flask_login import login_required
from flask import render_template

from ..auth.form import LoginForm

main_bp = Blueprint('main', __name__, url_prefix= '/main')


@main_bp.route('/index')
@login_required
def index():
    form = LoginForm()
    return render_template('auth/login.html', form=form)

