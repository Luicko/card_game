from __future__ import absolute_import
import pickle

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

    @property
    def is_playing(self):
        game = pickle.loads(session['game'])
        for player in game.participants:
            if player.player == self:
                return self._is_playing
    
    def play(card):
        for player in game.participants:
            if player.player == self:
                player.play(player.hand[card])

    def draw():
        for player in game.participants:
            if player.player == self:
                player.draw()
    
    def __repr__(self):
        return '<User %r>' % (self.username)

class Game(db.Model):
    __tablename__ = 'Game'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game = db.Column(db.String(255))

    """
    def set_game(game):
    game = game
    game.start_game()
    print (game, file=sys.stderr)
    print (game.act_player.player, file=sys.stderr)
    print (type(game), file=sys.stderr)
    global game
    """