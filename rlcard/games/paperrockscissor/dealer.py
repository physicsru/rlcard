from rlcard.games.base import Card
from rlcard.games.limitholdem import Dealer

class PaperrockscissorDealer(Dealer):
    def __init__(self, np_random):
        self.np_random = np_random
