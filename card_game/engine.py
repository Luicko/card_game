import random


class PlayerHand(object):

    def __init__(self, player, game, hand=None):
        self.player = player
        self.game = game
        self.hand = hand

    def play(self, card):
        if card not in self.hand:
            raise ValueError ("You don't have that card")
            
        self.game.play(player=self, card=card)
        self.hand.remove(card)

    def draw(self):
        self.hand.append(self.game.deal(self))


class CardGame(object):

    ranks = ['Sota', 'Copa', 'Moneda', 'Espada']
    values = ['1', '3', '4', '5', '6', '7', '8', '9', '10',
            'Principe', 'Caballo', 'Rey', '2']

    def __init__(self):
        self.participants = []
        self.winner = None
        self.act_player = 0
        self.last_player = 0
        self.last_card_played = 0
        self.stock = Stock(ranks=len(self.ranks), values=len(self.values))
        self.deck = []
        self.turn = None

    def start_game(self):
        initial_draw = int((len(self.stock.cards) * 0.5) / len(self.participants))

        if initial_draw == 0:
            initial_draw = 1

        for player in self.participants:
            cards = [self.stock.deal() for x in range(initial_draw)]
            player.hand = cards

        self.act_player = self.participants[0]
        self.turn = self.next_turn()

    def play(self, player, card):
        if player != self.act_player:
            raise ValueError ("It isn't your turn")

        if not self.last_card_played:
            self.deck.append(card)
            self.last_card_played = card
            self.last_player = self.act_player
            self.act_player = self.participants[self.turn]
            self.turn = self.next_turn()

        elif self.act_player == self.last_player or self.compare(other=card):
            self.deck.append(card)
            self.last_card_played = card
            self.last_player = self.act_player
            self.act_player = self.participants[self.turn]
            self.turn = self.next_turn()

        else:
            raise ValueError ("You can't make that play")

        if player.hand[-1] == player.hand[0]: 
            self.set_winner(player)


    def deal(self, player=None):
        if player and player != self.act_player:
            raise ValueError ("It isn't your turn")

        else:
            draw = self.stock.deal()

            if not draw:
                self.stock = Stock(self.deck)
                self.deal() 
            self.act_player = self.participants[self.turn]
            self.turn = self.next_turn()
            return draw

    def set_winner(self, player):
        self.winner = player.player
        self.participants = []

    def show_card(self, card):
        return '%r - %s' % (self.values[card.value], self.ranks[card.rank])

    def compare(self, other):
        if self.last_card_played.rank < other.rank:
            return 1

        elif self.last_card_played.rank == other.rank:
            if self.last_card_played.value < other.value:
                return 1

        else:
            return 0

    def player_quit(self, user):
        for player in self.participants:

            if player.player == user:
                leave = player

        self.participants.remove(leave)

        if self.participants[-1] == self.participants[0]:
            pass

        elif self.act_player == leave:
            self.turn = self.leave_turn_act()
            self.act_player = self.participants[self.turn]

        elif self.last_player == leave:
            self.last_player = self.participants[self.leave_turn_last()]

    def next_turn(self):
        return (self.participants.index(self.act_player) + 1) % len(self.participants)

    def leave_turn_act(self):
        return (self.participants.index(self.last_player) + 1) % len(self.participants)

    def leave_turn_last(self):
        return (self.participants.index(self.last_player) - 1) % len(self.participants)

    def add_player(self, player):
        self.participants.append(PlayerHand(player, game=self))


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