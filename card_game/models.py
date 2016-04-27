from __future__ import absolute_import
from __future__ import print_function # In python 2.7

from flask.ext.login import UserMixin

from . import db, app

player_game_table = db.Table('PlayerGame',
    db.Column('idplayer', db.Integer, db.ForeignKey('Player.id')),
    db.Column('idgamme', db.Integer, db.ForeignKey('Game.id')))

class Player(db.Model, UserMixin):
    __tablename__ = 'Player'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    score = db.Column(db.Integer)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def play(self, game, card):
        for player in game.participants:
            if player.player == self.username:
                player.play(player.hand[card])
                return game

    def draw(self, game):
        for player in game.participants:
            if player.player == self.username:
                player.draw()
                return game

    def hand(self, game):
        for player in game.participants:
            if player.player == self.username:
                return player.hand   
    
    def __repr__(self):
        return '<User %r>' % (self.username)

class Game(db.Model):
    __tablename__ = 'Game'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game = db.Column(db.String(10000))