import numpy as np
from copy import copy

from rlcard.games.paperrockscissor import Dealer
from rlcard.games.paperrockscissor import Player
from rlcard.games.paperrockscissor import Judger
from rlcard.games.paperrockscissor import Round

from rlcard.games.limitholdem import Game

class PaperrockscissorGame:
    def __init__(self, allow_step_back=False, num_players=2):
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = num_players
        self.history = []
        self.players = None
        self.judger = None
        self.game_pointer = None

    def configure(self, game_config):
        self.num_players = game_config['game_num_players']

    def init_game(self):
        # Initialize players and judger
        self.players = [Player(i, self.np_random) for i in range(self.num_players)]
        self.judger = Judger(self.np_random)
        
        # Randomly choose the starting player
        self.game_pointer = self.np_random.randint(0, self.num_players)

        state = self.get_state(self.game_pointer)
        return state, self.game_pointer

    def step(self, action):
        if self.allow_step_back:
            # Snapshot the current state
            gp = self.game_pointer
            ps = [copy(player) for player in self.players]
            self.history.append((gp, ps))

        # Apply the action and change the pointer to the next player
        self.players[self.game_pointer].action = action
        self.game_pointer = (self.game_pointer + 1) % self.num_players

        state = self.get_state(self.game_pointer)
        return state, self.game_pointer

    def get_state(self, player_id):
        # Construct the state for the given player
        legal_actions = ['rock', 'paper', 'scissors']
        state = {}

        # Include the player's own action (if any)
        state['player_action'] = self.players[player_id].action

        # If the game extends over multiple rounds, include previous round actions here
        # For example, state['past_actions'] = ...

        # Information about the current player and legal actions
        state['current_player'] = self.game_pointer
        state['legal_actions'] = legal_actions if self.game_pointer == player_id else []

        return state

    def is_over(self):
        # The game is over after each player has made a choice
        return all(player.action is not None for player in self.players)

    def get_payoffs(self):
        # Calculate the payoffs based on the players' actions
        return self.judger.judge_game(self.players)

    def step_back(self):
        if len(self.history) > 0:
            self.game_pointer, self.players = self.history.pop()
            return True
        return False

    def get_legal_actions(self):
        # All actions are legal at any point in the game
        return ['rock', 'paper', 'scissors']

