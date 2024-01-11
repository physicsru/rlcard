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

class KuhnEnv(Env):
    def __init__(self, config):
        self.name = 'kuhn'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = Game()
        super().__init__(config)
        self.actions = ['call', 'bet', 'fold', 'check']
        self.state_shape = [[6] for _ in range(self.num_players)]
        self.action_shape = [None for _ in range(self.num_players)]

        # Load card to index mapping (to be created)
        with open(os.path.join(rlcard.__path__[0], 'games/kuhn/card2index.json'), 'r') as file:
            self.card2index = json.load(file)

    def _get_legal_actions(self):
        legal_actions = self.game.get_legal_actions()
        return legal_actions  #[self.actions.index(action) for action in legal_actions]

    # _get_legal_actions, _extract_state, get_payoffs, _decode_action, get_perfect_information methods
    def _extract_state(self, state):
        # Initial state based on the card
        extracted_state = {}
        hand = state['hand_card']
        position = state['current_player']
        obs = self.card2index[hand.rank]
        action_recorder = [action for _, action in state['history']]
        legal_actions = OrderedDict({self.actions.index(a): None for a in state['legal_actions']})
        extracted_state['legal_actions'] = legal_actions
        # Adjust state based on actions for position 0
        obs = np.zeros(1)
        if position == 0:
            if 'bet' in action_recorder:
                obs += 3  # Adjusting the state for pass_bet

        # Adjust state based on actions for position 1
        elif position == 1:
            action_history = action_recorder
            if 'bet' in action_history:
                obs += (0 if action_history[-1] == 'bet' else 1)  # J_bet or J_pass
            else:
                obs += 2  # Adjusting for Q or K with pass or bet
        extracted_state['obs'] = obs

        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [a for a in state['legal_actions']]
        extracted_state['action_record'] = action_recorder
        return extracted_state
    
    def get_payoffs(self):
        return self.game.get_payoffs()
    
    def _decode_action(self, action_id):
        # legal_actions = self.game.get_legal_actions()
        # if self.actions[action_id] not in legal_actions:
        #     if 'check' in legal_actions:
        #         return 'check'
        #     else:
        #         return 'fold'
        return self.actions[action_id]
    
    def get_perfect_information(self):
        state = {}
        state['hand_card'] = [player.hand for player in self.game.players]
        state['chips'] = [self.game.players[i].in_chips for i in range(self.num_players)]
        state['current_round'] = self.game.round_counter
        #state['pot'] = self.game.pot
        state['current_player'] = self.game.game_pointer
        state['legal_actions'] = self.game.get_legal_actions()
        return state




