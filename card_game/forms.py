from flask.ext.wtf import Form
from wtforms import (StringField, PasswordField, validators)

class AddPlayer(Form):
	username = StringField('Username', validators=[validators.DataRequired()])
	password = PasswordField('Password', 
		[validators.Required(), 
		validators.EqualTo('confirm')])
	confirm = PasswordField('Repeat Password')

class LoginForm(Form):
    username = StringField('Username', validators=[
            validators.DataRequired()])
    password = PasswordField('Password')

class CreateRoom(Form):
	game_name = StringField('Game Name', validators=[
            validators.DataRequired()])