from . import main
from flask_login import login_required, current_user
from flask import render_template, redirect, flash, url_for
from ..model import User
from ..auth.form import LoginForm
from .form import ProfileForm
from ..db import db


@main.route('/index')
@login_required
def index():
    form = LoginForm()
    return render_template('auth/login.html', form=form)

#show profile
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@main.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.realname.data
        current_user.location = form.location.data
        current_user.about_me = form.aboutme.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated!')
        return redirect(url_for('.user', username=current_user.username))
    form.realname.data = current_user.name
    form.location.data = current_user.location
    form.aboutme.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

