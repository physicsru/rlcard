from rlcard.utils.utils import rank2int

class KuhnJudger:
    ''' The Judger class for Leduc Hold'em
    '''
    def __init__(self, np_random):
        ''' Initialize a judger class
        '''
        self.np_random = np_random

    @staticmethod
    def judge_game(players, history):
        #total_pot = 2  # Initial pot from antes
        #total_pot += sum(1 for _, action in history if action in ['bet', 'call'])
        rank_dict = {'J':0, 'Q':1, 'K':2}
        total = 0
        for p in players:
            total += p.in_chips
        
        for idx, player in enumerate(players):
            #ranks.append(rank2int(player.hand.rank))
            if player.status == 'folded':
                # The player who did not fold wins the pot
                fold_player_id = idx
                winner_id = 1 - fold_player_id
                #print("here ", winner_id, fold_player_id)
                # The loser loses the amount they put in the pot
                loser_chips = players[fold_player_id].in_chips
                winner_chips = total - loser_chips  # Winner's profit
                final_chips = min(abs(winner_chips), abs(loser_chips))

                payoffs = [final_chips if player.player_id == winner_id else -final_chips for player in players]
                return payoffs
            
        # if history[-1][1] == 'fold':
        #     # The player who did not fold wins the pot
        #     fold_player_id = history[-1][0]
        #     winner_id = 1 - fold_player_id
        #     #print("here ", winner_id, fold_player_id)
        #     # The loser loses the amount they put in the pot
        #     loser_chips = players[fold_player_id].in_chips
        #     winner_chips = total - loser_chips  # Winner's profit
        #     final_chips = min(abs(winner_chips), abs(loser_chips))

        #     payoffs = [final_chips if player.player_id == winner_id else -final_chips for player in players]
        #     return payoffs

        # Showdown: compare hands if no player folded
        player0_hand = players[0].hand
        player1_hand = players[1].hand

        if rank_dict[player0_hand.rank] > rank_dict[player1_hand.rank]:
            winner_id = 0
        elif rank_dict[player1_hand.rank] > rank_dict[player0_hand.rank]:
            winner_id = 1
        else:
            # Implement tie-breaking rules here if necessary
            return [0, 0]  # Example: Split pot


        fold_player_id = 1 - winner_id
        loser_chips = players[fold_player_id].in_chips
        winner_chips = total - loser_chips  # Winner's profit 
        final_chips = min(abs(winner_chips), abs(loser_chips))
        # print("win ", winner_id, fold_player_id)
        # print("chips ", winner_chips, loser_chips, total)
        # print(player0_hand, player1_hand)
        # print(rank_dict[player0_hand.rank], rank_dict[player1_hand.rank])
        # print(rank_dict[player0_hand.rank] > rank_dict[player1_hand.rank])
        # Assign payoffs based on the winner at showdown
        payoffs = []
        payoffs = [final_chips if player.player_id == winner_id else -final_chips for player in players]
        
        return payoffs
    
   
  
