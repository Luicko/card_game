from marshmallow import Schema, fields, post_load
from engine import *

class CardGameSchema(Schema):
    last_card_played = fields.Nested('CardSchema', default=None, allow_none=True)
    stock = fields.Nested('StockSchema')
    deck = fields.Nested('CardSchema', many=True)
    turn = fields.Integer()
    participants = fields.Nested('PlayerHandSchema', many=True)
    act_player = fields.Nested('PlayerHandSchema' , default=None, allow_none=True)
    last_player = fields.Nested('PlayerHandSchema' , default=None, allow_none=True)
    winner = fields.String(default=None, allow_none=True)

    @post_load
    def make_game(self, data):
        c = CardGame.__new__(CardGame)
        c.stock = data['stock']
        c.last_card_played = data['last_card_played']
        c.deck = data['deck']
        c.turn = data['turn']
        c.winner = None
        if 'participants' in data:
            x = 0
            c.participants = []
            c.last_player = data['last_player']            
            c.act_player = data['act_player']
            for p in data['participants']:
                c.participants.append(p)
                c.participants[x].game = c            
                x += 1
            for p in c.participants:
                if c.act_player.player == p.player:
                    c.act_player = p
                if c.last_player:
                    if c.last_player.player == p.player:
                        c.last_player = p
        return c


class StockSchema(Schema):
    cards = fields.Nested('CardSchema', many=True)

    @post_load
    def make_stock(self, data):
        return Stock(**data)

class CardSchema(Schema):
    rank = fields.Integer()
    value = fields.Integer()

    @post_load
    def make_card(self, data):
        if not data:
            pass
        else:
            return Card(**data)

class PlayerHandSchema(Schema):
    player = fields.String()
    hand = fields.Nested('CardSchema', many=True)

    @post_load
    def make_hand(self, data):
        if not data:
            pass
        else:
            ph = PlayerHand.__new__(PlayerHand)
            ph.player = data['player']
            ph.hand = []
            ph.game = None
            for card in data['hand']:
                ph.hand.append(card)
            return ph