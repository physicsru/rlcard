import unittest
from rlcard.games.kuhn.game import KuhnGame
from rlcard.games.kuhn.player import KuhnPlayer as Player
from rlcard.games.kuhn.judger import KuhnJudger as Judger
from rlcard.games.base import Card
import numpy as np

class TestKuhnMethods(unittest.TestCase):

    def setUp(self):
        self.game = KuhnGame()

    def test_get_num_actions(self):
        num_actions = self.game.get_num_actions()
        self.assertEqual(num_actions, 4)

    def test_init_game(self):
        state, player_id = self.game.init_game()
        self.assertEqual(player_id, self.game.get_player_id())
        self.assertIn('bet', state['legal_actions'])
        self.assertIn('check', state['legal_actions'])

    def test_step(self):
        self.game.init_game()
        self.game.step('bet')
        self.assertIn('call', self.game.get_legal_actions())
        self.assertIn('fold', self.game.get_legal_actions())
        #self.assertEqual(self.game.round.have_raised, 1)
        
        self.game.init_game()
        self.game.step('check')
        self.assertIn('bet', self.game.get_legal_actions())
        self.assertIn('check', self.game.get_legal_actions())
        #self.assertTrue(self.game.round.player_folded)

        self.game.init_game()
        self.game.step('bet')
        self.game.step('call')
        self.assertEqual(self.game.round_counter, 1)

        self.game.init_game()
        self.game.step('bet')
        self.game.step('fold')
        self.assertEqual(self.game.round_counter, 1)
        
        self.game.init_game()
        self.game.step('check')
        self.assertEqual(self.game.round_counter, 0)
        self.game.step('bet')
        self.assertEqual(self.game.round_counter, 0)
        self.game.step('fold')
        self.assertEqual(self.game.round_counter, 1)

    def test_judge_game(self):
        np_random = np.random.RandomState()
        self.game.init_game()
        players = [Player(0, np_random), Player(1, np_random)]
        players[0].hand = Card('S', 'J')
        players[1].hand = Card('S', 'Q')
        self.game.step('bet')
        self.game.step('fold') 
        payoffs = self.game.judger.judge_game(players, self.game.history)
        #print("payoffs = ", payoffs)
        self.assertEqual(payoffs[0], 1)
        self.assertEqual(payoffs[1], -1)
        
        self.game.init_game()
        self.game.players = [Player(0, np_random), Player(1, np_random)]
        self.game.players[0].hand = Card('S', 'K')
        self.game.players[1].hand = Card('S', 'Q')
        self.game.step('bet')
        #print("mark1, ", self.game.players[0].in_chips)
        self.game.step('call') 
        payoffs = self.game.judger.judge_game(self.game.players, self.game.history)
        #print("payoffs = ", payoffs)
        self.assertEqual(payoffs[0], 2)
        self.assertEqual(payoffs[1], -2)
        
        self.game.init_game()
        self.game.players = [Player(0, np_random), Player(1, np_random)]
        self.game.players[0].hand = Card('S', 'J')
        self.game.players[1].hand = Card('S', 'Q')
        self.game.step('bet')
        self.game.step('call') 
        payoffs = self.game.judger.judge_game(self.game.players, self.game.history)
        #print("payoffs = ", payoffs)
        self.assertEqual(payoffs[0], -2)
        self.assertEqual(payoffs[1], 2)
        
        self.game.init_game()
        self.game.players = [Player(0, np_random), Player(1, np_random)]
        self.game.players[0].hand = Card('S', 'J')
        self.game.players[1].hand = Card('S', 'Q')
        self.game.step('bet')
        self.game.step('fold') 
        payoffs = self.game.judger.judge_game(self.game.players, self.game.history)
        #print("payoffs = ", payoffs)
        self.assertEqual(payoffs[0], 1)
        self.assertEqual(payoffs[1], -1)
        
        self.game.init_game()
        self.game.players = [Player(0, np_random), Player(1, np_random)]
        self.game.players[0].hand = Card('S', 'J')
        self.game.players[1].hand = Card('S', 'Q')
        self.game.step('check')
        self.game.step('check') 
        payoffs = self.game.judger.judge_game(self.game.players, self.game.history)
        #print("payoffs = ", payoffs)
        self.assertEqual(payoffs[0], -1)
        self.assertEqual(payoffs[1], 1)
        
        self.game.init_game()
        self.game.players = [Player(0, np_random), Player(1, np_random)]
        self.game.players[0].hand = Card('S', 'Q')
        self.game.players[1].hand = Card('S', 'J')
        self.game.step('check')
        self.game.step('check') 
        payoffs = self.game.judger.judge_game(self.game.players, self.game.history)
        #print("payoffs = ", payoffs)
        self.assertEqual(payoffs[0], 1)
        self.assertEqual(payoffs[1], -1)
        
        self.game.init_game()
        self.game.players = [Player(0, np_random), Player(1, np_random)]
        self.game.players[0].hand = Card('S', 'Q')
        self.game.players[1].hand = Card('S', 'J')
        self.game.step('check')
        self.game.step('bet') 
        self.game.step('call')
        payoffs = self.game.judger.judge_game(self.game.players, self.game.history)
        #print("payoffs = ", payoffs)
        self.assertEqual(payoffs[0], 2)
        self.assertEqual(payoffs[1], -2)
        
        self.game.init_game()
        self.game.players = [Player(0, np_random), Player(1, np_random)]
        self.game.players[0].hand = Card('S', 'J')
        self.game.players[1].hand = Card('S', 'K')
        self.game.step('check')
        self.game.step('bet') 
        self.game.step('call')
        payoffs = self.game.judger.judge_game(self.game.players, self.game.history)
        #print("payoffs = ", payoffs)
        self.assertEqual(payoffs[0], -2)
        self.assertEqual(payoffs[1], 2)
        
        self.game.init_game()
        self.game.players = [Player(0, np_random), Player(1, np_random)]
        self.game.players[0].hand = Card('S', 'Q')
        self.game.players[1].hand = Card('S', 'J')
        self.game.step('check')
        self.game.step('bet') 
        self.game.step('fold')
        payoffs = self.game.judger.judge_game(self.game.players, self.game.history)
        #print("payoffs = ", payoffs)
        self.assertEqual(payoffs[0], -1)
        self.assertEqual(payoffs[1], 1)

       

    def test_is_over(self):
        self.game.init_game()
        self.game.step('check')
        self.game.step('bet')
        self.game.step('call')
        #print("round_counter", self.game.round_counter)
        #print(self.game.history)
        #print("here ", self.game.round.is_over())
        #print(self.game.round.action_history)
        self.assertTrue(self.game.is_over())
        
        
        self.game.init_game()
        self.game.step('check')
        self.game.step('check')
        # print("round_counter", self.game.round_counter)
        # print(self.game.history)
        # print("here ", self.game.round.is_over())
        # print(self.game.round.action_history)
        self.assertTrue(self.game.is_over())
        
        self.game.init_game()
        self.game.step('bet')
        self.game.step('call')
        # print("round_counter", self.game.round_counter)
        # print(self.game.history)
        # print("here ", self.game.round.is_over())
        # print(self.game.round.action_history)
        self.assertTrue(self.game.is_over())
        
        self.game.init_game()
        self.game.step('bet')
        self.game.step('fold')
        # print("round_counter", self.game.round_counter)
        # print(self.game.history)
        # print("here ", self.game.round.is_over())
        # print(self.game.round.action_history)
        self.assertTrue(self.game.is_over())
        
        self.game.init_game()
        self.game.step('check')
        self.game.step('bet')
        self.game.step('fold')
        # print("round_counter", self.game.round_counter)
        # print(self.game.history)
        # print("here ", self.game.round.is_over())
        # print(self.game.round.action_history)
        self.assertTrue(self.game.is_over())

if __name__ == '__main__':
    unittest.main()