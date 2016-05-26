#!/usr/bin/env python

from flask.ext.script import Manager, Server

from card_game import app, socketio

server = Server(host="0.0.0.0")
manager = Manager(app, server)

@manager.command
def clean():
    """
    Function designed for testin specific users and games
    """
    from card_game import db, models
    
    l = models.Player.query.filter_by(username='Luis').first()
    l.game_id = None
    db.session.add(l)
    db.session.commit()

    q = models.Player.query.filter_by(username='AQ').first()
    q.game_id = None
    db.session.add(q)
    db.session.commit()

    g = models.Game.query.first()
    db.session.delete(g)
    db.session.commit()

@manager.command
def run():
    """
    Function to enable the app to run under socket needs
    """
   socketio.run(app,
                host='127.0.0.1',
                port=5000,
                use_reloader=False)


if __name__ == "__main__":
    manager.run()