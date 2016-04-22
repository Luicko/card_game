import random
import itertools


POINTS_PER_GAME = 2


class PlayerHand(object):

    def __init__(self, player, cards, game):
        self.player = player
        self.game = game
        self.hand = cards

    def play(self, card):
        if card not in self.hand:
            raise ValueError ('You don\'t have that card')
        self.game.play(player=self, card=card)
        self.hand.remove(card)

    def draw(self):
        self.hand.append(self.game.deal())


class CardGame(object):

    ranks = ['Sota', 'Copa', 'Moneda', 'Espada']
    values = ['1', '3', '4', '5', '6', '7', '8', '9', '10',
            'Principe', 'Caballo', 'Rey', '2']

    def __init__(self, players):
        self.participants = []
        self.winner = None
        self.act_player = None
        self.last_player = None
        self.last_card_played = None
        self.stock = Stock(ranks=len(self.ranks), values=len(self.values))
        self.deck = []
        self.turns = None
        initial_draw = int((len(self.stock.cards) * 0.5) / len(players))
        if initial_draw == 0:
            initial_draw = 1
        for p in players:
            cards = [self.stock.deal() for x in range(initial_draw)]
            self.participants.append(PlayerHand(p, cards, game=self))

    def start_game(self):
        self.act_player = self.participants[0]
        self.turns = (self.participants.index(self.act_player) + 1) % len(self.participants)


    def play(self, player, card):
        if player != self.act_player:
            raise ValueError ('It isn\'nt your turn')
        if not self.last_card_played:
            self.deck.append(card)
            self.last_card_played = card
            self.last_player = self.act_player
            self.act_player = self.participants[self.turns]
            self.turns = (self.participants.index(self.act_player) + 1) % len(self.participants)
        elif player == self.last_player or self.compare(other=card):
            self.deck.append(card)
            self.last_card_played = card
            self.last_player = self.act_player
            self.act_player = self.participants[self.turns]
            self.turns = (self.participants.index(self.act_player) + 1) % len(self.participants)
        else:
            raise ValueError ("You can't make that play")
        if player.hand[-1] == player.hand[0]: 
            self.set_winner(player)


    def deal(self):
        draw = self.stock.deal()
        if not draw:
            self.stock = Stock(self.deck)
            self.deal() 
        self.act_player = self.participants[self.turns]
        self.turns = (self.participants.index(self.act_player) + 1) % len(self.participants)
        return draw

    def set_winner(self, player):
        self.winner = player

    def show_card(self, card):
        return (self.values[card.value] +' - '+ self.ranks[card.rank])

    def compare(self, other):
        if self.last_card_played.rank < other.rank:
            return 1
        elif self.last_card_played.rank == other.rank:
            if self.last_card_played.value < other.value:
                return 1
        else:
            return 0


class Stock(object):

    def __init__(self, cards=None, ranks=None, values=None):
        if not cards:
            self.cards = []
            self.create(ranks, values)
            self.shuffle()
        else:
            self.cards = cards

    def create(self, ranks, values):
        for rank in range(ranks):
            for value in range(values):
                self.cards.append(Card(rank=rank, value=value))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        try:
            return self.cards.pop()
        except IndexError:
            return None


class Card(object):

    def __init__(self, rank, value):
        self.rank = rank
        self.value = value