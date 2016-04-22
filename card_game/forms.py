from flask.ext.wtf import Form
from wtforms import (StringField, PasswordField, validators)

class AddPlayer(Form):
	username = StringField('Username', validators=[validators.DataRequired()])
	password = PasswordField('Password', 
        [validators.Required()])

class LoginForm(Form):
    username = StringField('Username', validators=[
            validators.DataRequired()])
    password = PasswordField('Password')