#!/usr/bin/env python

from flask.ext.script import Manager, Server

from card_game import app, socketio

server = Server(host="0.0.0.0")
manager = Manager(app, server)

@manager.command
def run():
   socketio.run(app,
                host='127.0.0.1',
                port=5000,
                use_reloader=False)


if __name__ == "__main__":
    manager.run()