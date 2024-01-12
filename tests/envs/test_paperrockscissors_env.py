import unittest
import numpy as np
import os
import rlcard
from rlcard.agents.random_agent import RandomAgent
from tests.envs.determism_util import is_deterministic
os.environ['KMP_DUPLICATE_LIB_OK']='True'

class TestKuhnEnv(unittest.TestCase):

    def test_reset_and_extract_state(self):
        env = rlcard.make('paperrockscissor')
        state, _ = env.reset()
        self.assertEqual(state['obs'].size, 1)
        print(state.keys())
        for action in state['legal_actions']:
            self.assertLess(action, env.num_actions)

    def test_is_deterministic(self):
        self.assertTrue(is_deterministic('paperrockscissor'))

    def test_get_legal_actions(self):
        env = rlcard.make('paperrockscissor')
        env.reset()
        legal_actions = env._get_legal_actions()
        #print("legal_actions ", legal_actions)
        for action in legal_actions:
            self.assertIn(action, env.actions)

    def test_decode_action(self):
        env = rlcard.make('paperrockscissor')
        state, _ = env.reset()
        for action in state['legal_actions']:
            decoded = env._decode_action(action)
            self.assertIn(decoded, env.actions)

    def test_step(self):
        env = rlcard.make('paperrockscissor')
        state, player_id = env.reset()
        self.assertEqual(player_id, env.get_player_id())
        action = list(state['legal_actions'].keys())[0]
        _, player_id = env.step(action)
        self.assertEqual(player_id, env.get_player_id())

    def test_run(self):
        env = rlcard.make('paperrockscissor')
        agents = [RandomAgent(env.num_actions) for _ in range(env.num_players)]
        env.set_agents(agents)
        trajectories, payoffs = env.run(is_training=False)
        self.assertEqual(len(trajectories), 2)
        total = 0
        for payoff in payoffs:
            total += payoff
        self.assertEqual(total, 0)

    def test_get_perfect_information(self):
        env = rlcard.make('paperrockscissor')
        _, player_id = env.reset()
        self.assertEqual(player_id, env.get_perfect_information()['current_player'])


if __name__ == '__main__':
    unittest.main()
