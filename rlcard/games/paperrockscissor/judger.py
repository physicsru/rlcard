from rlcard.utils.utils import rank2int


class PaperrockscissorJudger:
    def __init__(self, np_random):
        self.np_random = np_random

    @staticmethod
    def judge_game(players):
        ''' Judge the winner of the game.

        Args:
            players (list): The list of players who play the game

        Returns:
            (list): The payoffs for the players
        '''
        if len(players) != 2:
            raise ValueError("Rock-Paper-Scissors must be played with 2 players")

        action1 = players[0].action
        action2 = players[1].action
        print(action1, action2)

        if action1 == action2:
            # It's a tie
            return [0, 0]

        # Mapping of actions to what they can beat
        beats = {
            'rock': 'scissors',
            'scissors': 'paper',
            'paper': 'rock'
        }

        if beats[action1] == action2:
            # Player 1 wins
            return [1, -1]
        else:
            # Player 2 wins
            return [-1, 1]