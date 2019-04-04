from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..model import User
from . import auth
from .form import LoginForm, RegisterForm
from flask_login import current_user

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():   
        if User.query.filter_by(username=form.username.data).first():
            flash('The username is registered!')
            return render_template('auth/register.html', form=form)
        User.addUser(form.username.data, form.password.data)
        flash('Register Successfully!')
        return redirect(url_for('auth.login'))   
    return render_template('auth/register.html', form=form)
            
@auth.route('/login', methods = ['GET', 'POST']) 
def login():
    form = LoginForm()
    if form.validate_on_submit(): # check post data and get can't go in
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, form.remember_me.data) #record the current user in session
            next = request.args.get('next') # if the login operation is mandatory, once login, go to that page directly
            if not next:
                next = url_for('main.user', username=user.username)
            return redirect(next)
        flash('Invalid username or password!') 
    return render_template('auth/login.html', form=form)


@auth.route('/logout') 
@login_required
def logout():
    logout_user() #remove the record about the user
    flash('You have been logged out!')
    return redirect(url_for('auth.login'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping() #update the operation time
    
        
 
        
