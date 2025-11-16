from typing import List
from lib.strategic_form_game import TwoPlayerStrategicFormGame

class VickeryAuction():
    """
    Vickery Auction (known as second-price sealed-bid)
    """
    def __init__(self, theta_values: List[int], bids:List[int], tie_breacker: int):
        self.theta_values = theta_values
        self.bids = bids
        self.tie_breacker = tie_breacker

        self._strategic_form_game = VickeryAuction._build_strategic_form_game(bids, tie_breacker, theta_values)

    def _build_strategic_form_game(bids, tie_breacker, theta_values) -> TwoPlayerStrategicFormGame:
        player1_strategies = list([str(bid) for bid in bids])
        player2_strategies = list(player1_strategies)
        strategies = [player1_strategies, player2_strategies]

        payoffs = []
        for first_player_bid_index in range(len(bids)):
            first_player_bid = bids[first_player_bid_index]
            if len(payoffs) <= first_player_bid_index:
                payoffs.append([])

            for second_player_bid_index in range(len(bids)):
                second_player_bid = bids[second_player_bid_index]

                if first_player_bid > second_player_bid:
                    # first player utility: evaluation - pay
                    utility = theta_values[0] - second_player_bid
                    payoffs[first_player_bid_index].append((utility, 0))

                
                elif first_player_bid < second_player_bid:
                    # second player utility: evaluation - pay
                    utility = theta_values[1] - first_player_bid
                    payoffs[first_player_bid_index].append((0, utility))

                else: # tie
                    utility = theta_values[tie_breacker] - first_player_bid
                    payoff = [0, 0]
                    payoff[tie_breacker] = utility
                    payoffs[first_player_bid_index].append(tuple(payoff))

        return TwoPlayerStrategicFormGame(strategies, payoffs)

    def game(self):
        return self._strategic_form_game