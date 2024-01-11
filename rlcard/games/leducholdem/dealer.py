from rlcard.games.base import Card
from rlcard.games.limitholdem import Dealer

class KuhnPokerDealer(Dealer):
    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = [Card('S', 'J'), Card('S', 'Q'), Card('S', 'K')]
        self.shuffle()

    def shuffle(self):
        self.np_random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

