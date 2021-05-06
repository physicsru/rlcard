''' Wrrapers of pretrained models.
'''
import os

import rlcard
from rlcard.agents import CFRAgent
from rlcard.models.model import Model

# Root path of pretrianed models
ROOT_PATH = os.path.join(rlcard.__path__[0], 'models/pretrained')

class LeducHoldemNFSPModel(Model):
    ''' A pretrained PyTorch model on Leduc Holdem with NFSP
    '''
    def __init__(self):
        ''' Load pretrained model
        '''
        import torch
        from rlcard.agents import NFSPAgent
        env = rlcard.make('leduc-holdem')
        self.nfsp_agents = []
        for i in range(env.player_num):
            agent = NFSPAgent(scope='nfsp' + str(i),
                              action_num=env.action_num,
                              state_shape=env.state_shape,
                              hidden_layers_sizes=[128,128],
                              q_mlp_layers=[128,128],
                              device=torch.device('cpu'))
            self.nfsp_agents.append(agent)

        check_point_path = os.path.join(ROOT_PATH, 'leduc_holdem_nfsp_pytorch/model.pth')
        checkpoint = torch.load(check_point_path)
        for agent in self.nfsp_agents:
            agent.load(checkpoint)

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.nfsp_agents

class LeducHoldemCFRModel(Model):
    ''' A pretrained model on Leduc Holdem with CFR (chance sampling)
    '''
    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('leduc-holdem')
        self.agent = CFRAgent(env, model_path=os.path.join(ROOT_PATH, 'leduc_holdem_cfr'))
        self.agent.load()
    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return [self.agent, self.agent]

