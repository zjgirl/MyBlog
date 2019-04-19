from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField

class ProfileForm(FlaskForm):
    realname = StringField('Real name')
    location = StringField('Location')
    aboutme = TextAreaField('About me')

    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    body = PageDownField("What's on your mind?", validators = [DataRequired()])
    submit = SubmitField('Submit')

