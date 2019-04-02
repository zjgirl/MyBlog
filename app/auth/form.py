
# use wtf web, use wtf.quick_form() to render template
# no need to define form in the html

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('password_confirm', message='Passwords must be equal!')])
    password_confirm = PasswordField('Password_confirm', validators = [DataRequired()])

    submit = SubmitField('Register')