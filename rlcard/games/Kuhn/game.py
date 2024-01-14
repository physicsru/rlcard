import numpy as np
from copy import copy

from rlcard.games.kuhn import Dealer
from rlcard.games.kuhn import Player
from rlcard.games.kuhn import Judger
from rlcard.games.kuhn import Round

from rlcard.games.limitholdem import Game
ANTE_AMOUNT = 1
class KuhnGame(Game):
    def __init__(self, allow_step_back=False, num_players = 2):
        self.allow_step_back = allow_step_back
        self.np_random = np.random.RandomState()
        self.num_players = num_players
        # Initialize other necessary attributes

    # Methods: configure, init_game, step, get_state, is_over, get_payoffs, step_back
    def init_game(self):
        self.round_counter = 0
        self.dealer = Dealer(self.np_random)
        self.players = [Player(i, self.np_random) for i in range(self.num_players)]
        self.judger = Judger(self.np_random)
        for player in self.players:
            player.hand = self.dealer.deal_card()
            player.in_chips = ANTE_AMOUNT

        self.pot = 2  # Each player antes 1
        self.game_pointer = 0  # Player 0 starts
        self.history = []
        self.round = Round(self.num_players, self.np_random)
        self.round.start_new_round(0)
        #self.round = 1  # Round 1 of the game

        return self.get_state(self.game_pointer), self.game_pointer

    def step(self, action):
        if self.allow_step_back:
            # First snapshot the current state
            r = copy(self.round)
            r_raised = copy(self.round.raised)
            gp = self.game_pointer
            r_c = self.round_counter
            d_deck = copy(self.dealer.deck)
            #p = copy(self.public_card)
            action_history = copy(self.round.action_history)
            ps = [copy(self.players[i]) for i in range(self.num_players)]
            ps_hand = [copy(self.players[i].hand) for i in range(self.num_players)]
            self.history.append((r, r_raised, gp, r_c, d_deck, ps, ps_hand, action_history))
            
        #self.history.append((self.round.game_pointer, action))
        self.game_pointer = self.round.proceed_round(self.players, action)
        #next_player = self.round.game_pointer
        if self.round.is_over():
            self.round_counter += 1
            self.round.start_new_round(self.game_pointer)
        return self.get_state(self.game_pointer), self.game_pointer


    def is_over(self):
        alive_players = [1 if p.status=='alive' else 0 for p in self.players]
        # If only one player is alive, the game is over.
        if sum(alive_players) == 1:
            return True

        # If all rounds are finshed
        if self.round_counter >= 1:
            return True
        return False

    def get_payoffs(self):
        chips_payoffs = self.judger.judge_game(self.players, self.history)
        payoffs = np.array(chips_payoffs)
        return payoffs

    def get_state(self, player):
        # Implement this method to return the current game state from the perspective of the player_id
        chips = [self.players[i].in_chips for i in range(self.num_players)]
        legal_actions = self.get_legal_actions()
        state = self.players[player].get_state(chips, legal_actions)
        state['current_player'] = self.game_pointer
        #state['history'] = self.history
        state['hand_card'] = self.players[player].hand
        state['legal_actions'] = legal_actions
        return state
    
    def step_back(self):
        ''' Return to the previous state of the game

        Returns:
            (bool): True if the game steps back successfully
        '''
        if len(self.history) > 0:
            self.round, r_raised, self.game_pointer, self.round_counter, d_deck, self.players, ps_hand, action_history = self.history.pop()
            self.round.raised = r_raised
            self.round.action_history = action_history
            self.dealer.deck = d_deck
            for i, hand in enumerate(ps_hand):
                self.players[i].hand = hand
            return True
        return False