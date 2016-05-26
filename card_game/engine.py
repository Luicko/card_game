import random


class PlayerHand(object):
    """
    Class born from the relation of :class:`CardGame` and 
    a player that joined a game
    :param player: string of the player name
    :param game: :class:`CardGame`
    :param hand: list of :class:`Card` objects
    """
    def __init__(self, player, game, hand=None):
        self.player = player
        self.game = game
        self.hand = hand

    def play(self, card):
        """
        Method to allow the player to make a play in an specific game
        if the card is in his hand then allow 
        him/her to call :class:`CardGame`.:func:`play`
        :param card: :class:`Card` object
        """
        if card not in self.hand:
            raise ValueError ("You don't have that card")
            
        self.game.play(player=self, card=card)
        self.hand.remove(card)

    def draw(self):
        """
        Method for the player to get a new card
        """
        self.hand.append(self.game.deal(self))


class CardGame(object):
    """
    Main class for the game, containts all the information about a current game
    """

    ranks = ['Sota', 'Copa', 'Moneda', 'Espada']
    values = ['1', '3', '4', '5', '6', '7', '8', '9', '10',
            'Principe', 'Caballo', 'Rey', '2']

    def __init__(self):
        """
        :param participants: list of :class:`PlayerHand` objects
        :param winner: the player who won the game
        :param act_player: :class:`PlayerHand` instance
        :param last_player: :class:`PlayerHand` instance
        :param last_card_player: :class:`Card` instance
        :param stock: :class:`Stock` instance
        :param deck: list of :class:`Card` instances
        :param turn: index number of the participants
        """
        self.participants = []
        self.winner = None
        self.act_player = 0
        self.last_player = 0
        self.last_card_played = 0
        self.stock = Stock(ranks=len(self.ranks), values=len(self.values))
        self.deck = []
        self.turn = None

    def start_game(self):
        """
        Method to allow the game to be played, sets the cards for the player
        and turns
        """
        initial_draw = int((len(self.stock.cards) * 0.5) / len(self.participants))

        if initial_draw == 0:
            initial_draw = 1

        for player in self.participants:
            cards = [self.stock.deal() for x in range(initial_draw)]
            player.hand = cards

        self.act_player = self.participants[0]
        self.turn = self.next_turn()

    def play(self, player, card):
        """
        Method call by the :class:`PLayerHand` to play a card
        Raises error if the :class:`Card` or the player are not allowed
        :param player: :class:`PlayerHand` instance
        :param card: :class:`Card` instance
        """
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
        """
        Method called by the :class:`PlayerHand` to get a new :class:`Card` instance
        """
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
        """
        Method to translate the :class:`Card` instance into a string
        :return: string of values
        """
        return '%r - %s' % (self.values[card.value], self.ranks[card.rank])

    def compare(self, other):
        """
        Compares the cards that wants to be played against the last_card_played
        :param other: :class:`Card` instance
        :return: True or False
        """
        if self.last_card_played.rank < other.rank:
            return 1

        elif self.last_card_played.rank == other.rank:
            if self.last_card_played.value < other.value:
                return 1

        else:
            return 0

    def player_quit(self, user):
        """
        Method designed to take a :class:`PlayerHand` instance from participants
        and adjust the turns to the new size of the list
        :param user: player name
        """
        for player in self.participants:

            if player.player == user:
                leave = player

        self.participants.remove(leave)

        if self.participants:
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
    """
    Class for the deck that-s going to be used on a game
    """

    def __init__(self, cards=None, ranks=None, values=None):
        """
        :param cards: list of :class:`Card` instances
        :param ranks: list of integers
        :param values: list of integers and string
        """
        if not cards:
            self.cards = []
            self.create(ranks, values)
            self.shuffle()

        else:
            self.cards = cards

    def create(self, ranks, values):
        """
        Method to create the list of :class:`Card` instances based on
        the rank and value
        """
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