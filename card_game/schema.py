from marshmallow import Schema, fields, post_load
from engine import *

class CardGameSchema(Schema):
    """
    Basic schema of a :class:`CardGame` to be able to json its content
    """
    last_card_played = fields.Nested('CardSchema', default=None, allow_none=True)
    stock = fields.Nested('StockSchema')
    deck = fields.Nested('CardSchema', many=True)
    turn = fields.Integer(default=None, allow_none=True)
    participants = fields.Nested('PlayerHandSchema', many=True, default=None, allow_none=True)
    act_player = fields.Nested('PlayerHandSchema' , default=None, allow_none=True)
    last_player = fields.Nested('PlayerHandSchema' , default=None, allow_none=True)
    winner = fields.String(default=None, allow_none=True)

    @post_load
    def make_game(self, data):
        """
        Special function recreate an existing :class:`CardGame` instance
        :param data: metadata of a game
        :return: :class:`CardGame` instance
        """
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

            if c.last_player or c.act_player:
                for p in c.participants:
                    if c.act_player.player == p.player:
                        c.act_player = p

                    if c.last_player:
                        if c.last_player.player == p.player:
                            c.last_player = p
        return c


class StockSchema(Schema):
    """
    Basic schema for a :class:`Stock` instance inside a :class:`CardGame` instance
    """
    cards = fields.Nested('CardSchema', many=True)

    @post_load
    def make_stock(self, data):
        return Stock(**data)


class CardSchema(Schema):
    """
    Basic schema for a :class:`Card`
    """
    rank = fields.Integer()
    value = fields.Integer()

    @post_load
    def make_card(self, data):
        if not data:
            pass

        else:
            return Card(**data)


class PlayerHandSchema(Schema):
    """
    Schema for a :class:`PlayerHand` instance insde a :class:`CardGame` instance
    """
    player = fields.String()
    hand = fields.Nested('CardSchema', many=True, allow_none=True)

    @post_load
    def make_hand(self, data):
        """
        Function to recreate a :class:`PlayerHand` instance
        :param data: metada for a player
        :return: :class:`PlayerHand` instance
        """
        if not data:
            pass

        else:
            ph = PlayerHand.__new__(PlayerHand)
            ph.player = data['player']
            ph.hand = []
            ph.game = None
            
            if data['hand']:
                for card in data['hand']:
                    ph.hand.append(card)
            return ph