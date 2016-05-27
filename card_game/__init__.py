#async desgined for socket functionability
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

from flask import Flask, request
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mysql import MySQL
from flask.ext.socketio import SocketIO
from flask_bootstrap import Bootstrap

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('card_game.settings')
app.config.from_pyfile('settings.conf')
socketio = SocketIO(app, async_mode=async_mode)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

Bootstrap(app)
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