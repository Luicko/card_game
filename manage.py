#!/usr/bin/env python

from flask.ext.script import Manager, Server

from card_game import app

server = Server(host="0.0.0.0")
manager = Manager(app, server)
manager.add_command("runserver", server)


if __name__ == "__main__":
    manager.run()