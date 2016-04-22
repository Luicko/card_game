from __future__ import print_function # In python 2.7
import sys

from flask import (render_template, redirect, url_for, 
    request, g, flash, session)
from flask.ext.login import (login_user, logout_user, current_user,
    login_required)
from werkzeug.security import generate_password_hash, \
     check_password_hash

from . import engine, app, db
from .forms import AddPlayer, LoginForm
from engine import *
from .models import Player, Game

def set_game(games):
    game = games
    game.start_game()
    global game

def is_playing(user ,game):
        for player in game.participants:
            if player.player == user.username:
                return True

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def regist():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AddPlayer()
    if form.validate_on_submit():
        u = Player(username=form.username.data, 
            password=generate_password_hash(form.password.data))
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('addplayer.html', form=form, title='Sign Up')

@app.route('/sign in', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        u = Player.query.filter_by(username=form.username.data).first()
        if not u:
            return redirect(url_for('login'))
        elif check_password_hash(u.password, form.password.data):
            login_user(u)
            return redirect(url_for('index'))
    return render_template('login.html', form=form, title='Sign In')

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))

@app.route('/preparation', methods=['GET', 'POST'])
def preparation():
    player_list = Player.query.all()
    try:
        if game:
            if is_playing(current_user, game):
                return redirect('playing')
    except NameError:
        pass
    return render_template('preparation.html', player_list=player_list)

@app.route('/ready', methods=['GET', 'POST'])
def ready():
    player_list = request.form.getlist("add")
    set_game(CardGame(player_list))
    return redirect(url_for('playing'))

@app.route('/playing')
def playing():
    if game.winner == None:
        return render_template('playing.html', game=game)
    else:
        return redirect(url_for('winner'))

@app.route('/play/<card>', methods=['POST', 'GET'])
def play(card):
    try:
        current_user.play(game, int(card))
        return redirect(url_for('playing'))
    except ValueError as error:
        flash(str(error))
        return redirect('/playing')

@app.route('/draw')
def draw():
    current_user.draw(game)
    return redirect('/playing')

@app.route('/winner')
def winner():
    return render_template('winner.html', game=game)