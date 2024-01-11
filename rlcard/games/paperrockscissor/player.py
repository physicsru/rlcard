class PaperrockscissorPlayer:
    def __init__(self, player_id, np_random):
        self.np_random = np_random
        self.player_id = player_id
        self.status = 'alive'
        self.action = None  # Player's chosen action

    def get_state(self, legal_actions):
        # Return the player's state, mainly their chosen action
        state = {
            'action': self.action,  # The player's chosen action
            'legal_actions': legal_actions  # Possible actions the player can take
        }
        return state
    
    def get_player_id(self):
        return self.player_id
