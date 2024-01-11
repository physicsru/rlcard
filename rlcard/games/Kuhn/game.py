import numpy as np
from copy import copy

from rlcard.games.kuhn import Dealer
from rlcard.games.kuhn import Player
from rlcard.games.kuhn import Judger
from rlcard.games.kuhn import Round

from rlcard.games.limitholdem import Game

class KuhnPokerGame(Game):
    def __init__(self, allow_step_back=False):
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = DEFAULT_GAME_CONFIG['game_num_players']
        # Initialize other necessary attributes

    # Methods: configure, init_game, step, get_state, is_over, get_payoffs, step_back
