# -*- coding: utf-8 -*-
''' Implement Kuhn Round class
'''

class KuhnRound:
    def __init__(self, num_players, np_random):
        self.np_random = np_random
        self.game_pointer = None
        self.num_players = num_players
        self.action_history = []

    def start_new_round(self, game_pointer):
        self.game_pointer = game_pointer
        self.action_history = []

    def proceed_round(self, players, action):
        # Check if the action is legal
        if action not in self.get_legal_actions():
            raise Exception(f'{action} is not a legal action.')

        # Record action and update player state
        self.action_history.append((self.game_pointer, action))
        if action in ['bet', 'call']:
            players[self.game_pointer].in_chips += 1
        elif action == 'fold':
            players[self.game_pointer].status = 'folded'

        # Update game pointer
        self.game_pointer = (self.game_pointer + 1) % self.num_players

        return self.game_pointer

    def get_legal_actions(self):
        actions_taken = [action for _, action in self.action_history]

        # Player one can check or bet
        if len(actions_taken) == 0:
            return ['check', 'bet']

        # Player two's action after player one checks
        if actions_taken == ['check']:
            return ['check', 'bet']

        # Actions after a bet has been made
        if 'bet' in actions_taken:
            return ['call', 'fold']

        return []

    def is_over(self):
        # Round is over if both players check, or if a bet is called or a player folds
        actions_taken = [action for _, action in self.action_history]
        if len(self.action_history) >= 2:
            last_two_actions = actions_taken[-2:]
            #print("last_two_actions = ", last_two_actions)
            #print()
            if last_two_actions == ['check', 'check'] or ('bet' in last_two_actions and 'call' in last_two_actions):
                return True
            if any(action == 'fold' for action in last_two_actions):
                return True
        return False
