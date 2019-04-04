from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField

class ProfileForm(FlaskForm):
    realname = StringField('Real name')
    location = StringField('Location')
    aboutme = TextAreaField('About me')

    submit = SubmitField('Submit')

