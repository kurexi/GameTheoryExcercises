from typing import List, Tuple

StrategyMatrix = List[List[str]]
Payoff = Tuple[int, int]
PayoffMatrix = List[List[Payoff]]

class TwoPlayerStrategicFormGame:
    """A class representing a strategic form game for **two players**"""

    """
    Initialize the strategic form game with players and their strategies.
    strategis for two player:

    [[player1_strategy1, player1_strategy2, ...],
     [player2_strategy1, player2_strategy2, ...]]

    """
    strategies: StrategyMatrix = []

    """ 
    Payoffs for two players for each combination of strategies:
    
    |                    | player2_strategy1                | player2_strategy2               | ...
    |--------------------|----------------------------------|---------------------------------|----
    | player1_strategy1  | (player1_payoff, player2_payoff) | (player1_payoff, player2_payoff)| ...
    |--------------------|----------------------------------|---------------------------------|----
    | player1_strategy2  | (player1_payoff, player2_payoff) | (player1_payoff, player2_payoff)| ...
    |--------------------|----------------------------------|---------------------------------|----
    | ...                | ...                              |  ...                            |

    [[(player1_payoff, player2_payoff), ...],
     [(player1_payoff, player2_payoff), ...],
     ...]
    """
    payoffs: PayoffMatrix = []

    def __init__(self, strategies: StrategyMatrix = None, payoffs: PayoffMatrix = None):
        if strategies is not None:
            self.strategies = strategies
        if payoffs is not None:
            self.payoffs = payoffs

    def get_weakly_dominant_strategies(self) -> List[tuple]:
        player1 = self._get_weakly_dominant_strategies_for_player(0)
        player2 = self._get_weakly_dominant_strategies_for_player(1)

        return player1 + player2
    
    def eliminate_weakly_dominated_strategies(self, print_process=False):
        weakly_dominant_strategies = self.get_weakly_dominant_strategies()
        if len(weakly_dominant_strategies) > 0:
            
            target_remove = weakly_dominant_strategies[0][1]
    
            result_strategies = [[],[]]
            for s1 in self.strategies[0]:
                if s1 != target_remove:
                    result_strategies[0].append(s1)

            for s2 in self.strategies[1]:
                if s2 != target_remove:
                    result_strategies[1].append(s2)

            sgame = self.subgame(result_strategies)
            if print_process:
                print("-----------------")
                print(f"Removing {target_remove} due to {weakly_dominant_strategies[0]}")
                sgame.print()
            return sgame.eliminate_weakly_dominated_strategies(print_process)

        return self


    def _get_weakly_dominant_strategies_for_player(self, player_index) -> List[tuple]:
        result = [];
        for i in range(len(self.strategies[player_index])):
            for j in range(len(self.strategies[player_index])):
                if i == j:
                    continue

                opponent_index = self._get_opponent(player_index)

                # 1. all utility values are as better as the other one
                atleast_equal = True;
                for o in range(len(self.strategies[opponent_index])):
                    if self._get_payoff(player_index, i, o)[player_index] < self._get_payoff(player_index, j, o)[player_index]:
                        atleast_equal = False
                        break

                if not atleast_equal:
                    continue

                # 1. Not equal
                equal = True
                for o in range(len(self.strategies[opponent_index])):
                    if self._get_payoff(player_index, i, o)[player_index] > self._get_payoff(player_index, j, o)[player_index]:
                        equal = False
                        break
                
                if equal:
                    continue

                result.append((self.strategies[player_index][i], self.strategies[player_index][j]))
        return result
    
    def _get_payoff(self, caller_index, caller_strategy_index, opponent_strategy_index) -> Payoff:
        if (caller_index == 0):
            return self.payoffs[caller_strategy_index][opponent_strategy_index]
        return self.payoffs[opponent_strategy_index][caller_strategy_index]

    def _get_opponent(self, player_index):
        return 1 - player_index


    def subgame(self, substrategies:StrategyMatrix):
        strategy_indexs = self._strategies_to_indexes(substrategies)
        subpayoff_matrix = self._subpayoff_matrix(strategy_indexs)

        return TwoPlayerStrategicFormGame(substrategies, subpayoff_matrix)

    def _strategies_to_indexes(self, strategies:StrategyMatrix):
        strategy_indexs = [[],[]]
        for player_index in [0, 1]:
            for player_strategy in strategies[player_index]:
                for i in range(len(self.strategies[player_index])):
                    if player_strategy == self.strategies[player_index][i]:
                        strategy_indexs[player_index].append(i)

        return strategy_indexs
    
    def _subpayoff_matrix(self, substrategy_indexs:StrategyMatrix) -> PayoffMatrix:
        result:PayoffMatrix = [];
        for i in range(len(substrategy_indexs[0])):
            result.append([])
            mappd_first_player_strategy_index = substrategy_indexs[0][i]
            for j in range(len(substrategy_indexs[1])):
                mappd_second_player_strategy_index = substrategy_indexs[1][j]
                tuple = self.payoffs[mappd_first_player_strategy_index][mappd_second_player_strategy_index]
                result[i].append(tuple)
        return result

    def print(self):
        from lib.printable_strategic_form_game import PrintableTwoPlayerStrategicFormGame
        print(PrintableTwoPlayerStrategicFormGame.from_game(self))