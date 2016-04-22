from flask import Flask, request
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mysql import MySQL

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('card_game.settings')
app.config.from_pyfile('settings.conf')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

db = SQLAlchemy(app)

from . import models, views, settings

@lm.user_loader
def load_user(id):
    """
    LoginManager callback to assign `current_user` proxy object.

    :param id: User ID
    :returns: :class:`User`
    """
    return models.Player.query.get(int(id))