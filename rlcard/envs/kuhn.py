import json
import os
import numpy as np
from collections import OrderedDict

import rlcard
from rlcard.envs import Env
from rlcard.games.kuhn import Game
from rlcard.utils import *

DEFAULT_GAME_CONFIG = {
        'game_num_players': 2,
        }

class KuhnPokerEnv(Env):
    def __init__(self, config):
        self.name = 'kuhn-poker'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = Game()
        super().__init__(config)
        self.actions = ['call', 'bet', 'fold', 'check']
        self.state_shape = [[6] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

        # Load card to index mapping (to be created)
        with open(os.path.join(rlcard.__path__[0], 'games/kuhn_poker/card2index.json'), 'r') as file:
            self.card2index = json.load(file)

    def _get_legal_actions(self):
        legal_actions = self.game.get_legal_actions()
        return [self.actions.index(action) for action in legal_actions]

    # _get_legal_actions, _extract_state, get_payoffs, _decode_action, get_perfect_information methods
    def _extract_state(self, state):
        extracted_state = {}

        # Encode legal actions
        legal_actions = OrderedDict({self.actions.index(a): None for a in state['legal_actions']})
        extracted_state['legal_actions'] = legal_actions

        # Encode own hand
        hand = state['hand']
        obs = [self.card2index[hand]]

        # Encode action history
        # Assuming each action is encoded as an integer
        action_history = self.action_recorder.record  # A list of actions
        obs.extend(action_history)

        extracted_state['obs'] = obs

        # Raw observation and legal actions for additional information
        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [a for a in state['legal_actions']]

        return extracted_state

    
    def get_payoffs(self):
        return self.game.get_payoffs()
    
    def _decode_action(self, action_id):
        return self.actions[action_id]
    
    def get_perfect_information(self):
        state = {}
        state['hands'] = [player.hand for player in self.game.players]
        state['pot'] = self.game.pot
        state['current_player'] = self.game.game_pointer
        state['legal_actions'] = self.game.get_legal_actions()
        return state




