import unittest
from rlcard.games.paperrockscissor.game import PaperrockscissorGame
from rlcard.games.paperrockscissor.player import PaperrockscissorPlayer as Player
from rlcard.games.paperrockscissor.judger import PaperrockscissorJudger as Judger
from rlcard.games.base import Card
import numpy as np

class TestPaperrockscissorMethods(unittest.TestCase):

    def setUp(self):
        self.game = PaperrockscissorGame()

    def test_get_num_actions(self):
        num_actions = self.game.get_num_actions()
        self.assertEqual(num_actions, 3)

    def test_init_game(self):
        state, player_id = self.game.init_game()
        self.assertEqual(player_id, self.game.get_player_id())
        self.assertIn('rock', state['legal_actions'])
        self.assertIn('scissors', state['legal_actions'])

    def test_judge_game(self):
        np_random = np.random.RandomState()
        self.game.init_game()
        players = [Player(0, np_random), Player(1, np_random)]
        self.game.step('rock')
        self.game.step('scissors') 
        payoffs = self.game.judger.judge_game(self.game.players)
        #print("payoffs = ", payoffs)
        self.assertEqual(payoffs[0], 1)
        self.assertEqual(payoffs[1], -1)
        
        self.game.init_game()
        self.game.players = [Player(0, np_random), Player(1, np_random)]
        self.game.step('rock')
        self.game.step('paper') 
        payoffs = self.game.judger.judge_game(self.game.players)
        #print("payoffs = ", payoffs)
        self.assertEqual(payoffs[0], -1)
        self.assertEqual(payoffs[1], 1)
        
        self.game.init_game()
        self.game.players = [Player(0, np_random), Player(1, np_random)]
        self.game.step('rock')
        self.game.step('scissors') 
        payoffs = self.game.judger.judge_game(self.game.players)
        #print("payoffs = ", payoffs)
        self.assertEqual(payoffs[0], 1)
        self.assertEqual(payoffs[1], -1)
       

    def test_is_over(self):
        self.game.init_game()
        self.game.step('rock')
        self.game.step('scissors')
        self.assertTrue(self.game.is_over())
        #self.game.step('paper')
        
        
        self.game.init_game()
        self.game.step('scissors')
        # print("round_counter", self.game.round_counter)
        # print(self.game.history)
        # print("here ", self.game.round.is_over())
        # print(self.game.round.action_history)
        self.assertFalse(self.game.is_over())
        
       

if __name__ == '__main__':
    unittest.main()