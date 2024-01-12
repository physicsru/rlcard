import json
import os
import numpy as np
from collections import OrderedDict

import rlcard
from rlcard.envs import Env
from rlcard.games.paperrockscissor import Game
from rlcard.utils import *

DEFAULT_GAME_CONFIG = {
        'game_num_players': 2,
        }

class PaperrockscissorEnv(Env):
    ''' Rock-Paper-Scissors Environment
    '''

    def __init__(self, config):
        ''' Initialize the Rock-Paper-Scissors environment
        '''
        self.name = 'rock-paper-scissors'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = Game()
        super().__init__(config)
        self.actions = ['rock', 'paper', 'scissors']
        # Define state shape based on game requirements
        self.state_shape = [[6] for _ in range(self.num_players)] #[[...]]  # Update this based on your state representation
        self.action_shape = [None for _ in range(self.num_players)]

    def _get_legal_actions(self):
        ''' Get all legal actions
        '''
        return self.game.get_legal_actions()

    def _extract_state(self, state):
        ''' Extract the state representation from state dictionary for agent
        '''
        extracted_state = {}
        extracted_state['legal_actions'] = {self.actions.index(a): None for a in self.actions}
        
        # Update this to include history or other relevant information
        obs = np.zeros(1)
        #print(state)
            
        extracted_state['obs'] = obs

        extracted_state['raw_obs'] = state
        extracted_state['raw_legal_actions'] = [a for a in self.actions]
        extracted_state['action_record'] = self.action_recorder

        return extracted_state

    def get_payoffs(self):
        ''' Get the payoff of a game
        '''
        return self.game.get_payoffs()

    def _decode_action(self, action_id):
        ''' Decode the action for applying to the game
        '''
        return self.actions[action_id]

    def get_perfect_information(self):
        ''' Get the perfect information of the current state
        '''
        # Assuming 'game' has a method to return the last actions
        state = {}
        state['legal_actions'] = self.game.get_legal_actions()
        state['current_player'] = self.game.game_pointer
        return state
    
