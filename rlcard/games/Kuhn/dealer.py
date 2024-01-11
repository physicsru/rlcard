from rlcard.games.base import Card
from rlcard.games.limitholdem import Dealer

class KuhnDealer(Dealer):

    def __init__(self, np_random):
        ''' Initialize a leducholdem dealer class
        '''
        self.np_random = np_random
        self.deck = [Card('S', 'J'), Card('S', 'Q'), Card('S', 'K')]
        self.shuffle()
        self.pot = 0
