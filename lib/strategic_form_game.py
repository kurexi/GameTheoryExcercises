from typing import List, Tuple

StrategyMatrix = List[List[str]]
Payoff = Tuple[int, int]
PayoffMatrix = List[List[Payoff]]

class TwoPlayerStrategicFormGame:
    """A class representing a strategic form game for **two players**.

    Strategies for the two players are arranged as a two-row matrix:

        [[player1_strategy1, player1_strategy2, ...],
         [player2_strategy1, player2_strategy2, ...]]

    Payoffs for every profile are provided as tuples (player1, player2):

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

    first_player = 0
    second_player = 1
    players = [first_player, second_player]

    def __init__(self, strategies: StrategyMatrix = None, payoffs: PayoffMatrix = None):
        """Initialize the game with optional strategy and payoff matrices.

        Args:
            strategies: Two-row matrix of strategy names where row 0 belongs to
                player 1 (rows) and row 1 to player 2 (columns).
            payoffs: Matrix of payoff tuples aligned with the strategies matrix,
                i.e., payoffs[i][j] corresponds to (p1, p2) for (row i, column j).
        """
        if strategies is not None:
            # strategies[0] -> player 1 actions, strategies[1] -> player 2 actions
            self._strategies = strategies
        if payoffs is not None:
            # payoffs[i][j] stores (player1, player2) for strategies (i, j)
            self._payoffs = payoffs

    def get_weakly_dominant_strategies(self) -> List[tuple]:
        player1 = self._get_weakly_dominant_strategies_for_player(0)
        player2 = self._get_weakly_dominant_strategies_for_player(1)

        return player1 + player2
    
    def eliminate_weakly_dominated_strategies(self, print_process=False):
        weakly_dominant_strategies = self.get_weakly_dominant_strategies()
        if len(weakly_dominant_strategies) > 0:
            
            target_remove = weakly_dominant_strategies[0][1]
    
            result_strategies = [[],[]]
            for s1 in self._strategies[self.first_player]:
                if s1 != target_remove:
                    result_strategies[self.first_player].append(s1)

            for s2 in self._strategies[self.second_player]:
                if s2 != target_remove:
                    result_strategies[self.second_player].append(s2)

            sgame = self.subgame(result_strategies)
            if print_process:
                print("-----------------")
                print(f"Removing {target_remove} due to {weakly_dominant_strategies[0]}")
                sgame.print()
            return sgame.eliminate_weakly_dominated_strategies(print_process)

        return self


    def _get_weakly_dominant_strategies_for_player(self, player_index) -> List[tuple]:
        result = [];
        for i in range(len(self._strategies[player_index])):
            for j in range(len(self._strategies[player_index])):
                if i == j:
                    continue

                opponent_index = self._get_opponent(player_index)

                # 1. all utility values are as better as the other one
                atleast_equal = True;
                for o in range(len(self._strategies[opponent_index])):
                    if self._get_payoff_value(player_index, i, o) < self._get_payoff_value(player_index, j, o):
                        atleast_equal = False
                        break

                if not atleast_equal:
                    continue

                # 1. Not equal
                equal = True
                for o in range(len(self._strategies[opponent_index])):
                    if self._get_payoff_value(player_index, i, o) > self._get_payoff_value(player_index, j, o):
                        equal = False
                        break
                
                if equal:
                    continue

                result.append((self._strategies[player_index][i], self._strategies[player_index][j]))
        return result
    
    def _get_payoff(self, caller_index, caller_strategy_index, opponent_strategy_index) -> Payoff:
        if (caller_index == self.first_player):
            return self._payoffs[caller_strategy_index][opponent_strategy_index]
        return self._payoffs[opponent_strategy_index][caller_strategy_index]
    
    def _get_payoff_value(self, caller_index, caller_strategy_index, opponent_strategy_index) -> int:
        return self._get_payoff(caller_index, caller_strategy_index, opponent_strategy_index)[caller_index]

    def _get_opponent(self, player_index):
        return 1 - player_index


    def subgame(self, substrategies:StrategyMatrix):
        strategy_indexs = self._strategies_to_indexes(substrategies)
        subpayoff_matrix = self._subpayoff_matrix(strategy_indexs)

        return TwoPlayerStrategicFormGame(substrategies, subpayoff_matrix)

    def _strategies_to_indexes(self, strategies:StrategyMatrix) -> list[list[int]]:
        strategy_indexs = [[],[]]
        for player_index in self.players:
            for player_strategy in strategies[player_index]:
                for i in range(len(self._strategies[player_index])):
                    if player_strategy == self._strategies[player_index][i]:
                        strategy_indexs[player_index].append(i)

        return strategy_indexs
    
    def _strategy_to_index(self, strategy: str):
        for i in self.players:
            for j in range(len(self._strategies[i])):
                if strategy == self._strategies[i][j]:
                    return j
                
        raise ValueError(f"Strategy {strategy} not found in any player's strategies.")
    
    def _subpayoff_matrix(self, substrategy_indexs:StrategyMatrix) -> PayoffMatrix:
        result:PayoffMatrix = [];
        for i in range(len(substrategy_indexs[self.first_player])):
            result.append([])
            mappd_first_player_strategy_index = substrategy_indexs[self.first_player][i]
            for j in range(len(substrategy_indexs[1])):
                mappd_second_player_strategy_index = substrategy_indexs[self.second_player][j]
                tuple = self._payoffs[mappd_first_player_strategy_index][mappd_second_player_strategy_index]
                result[i].append(tuple)
        return result

    def print(self):
        from lib.printable_strategic_form_game import PrintableTwoPlayerStrategicFormGame
        print(PrintableTwoPlayerStrategicFormGame.from_game(self))

    def pure_nash_equilibria(self):
        best_responses = [[],[]]
        for player_index in self.players:
            for opponent_strategy in self._strategies[self._get_opponent(player_index)]:
                for response in self.best_responses(player_index, opponent_strategy):
                    best_responses[player_index].append((response, opponent_strategy))

        result = []
        for first_player_response in best_responses[self.first_player]:
            for second_player_response in best_responses[self.second_player]:
                if first_player_response[0] == second_player_response[1] and first_player_response[1] == second_player_response[0]:
                    result.append(first_player_response)
        
        return result

    def best_responses(self, caller_index: int, opponets_strategy: str) -> List[str]:
        response_indexes = []
        caller_strategies = self._strategies[caller_index] 
        opponent_strategy_index = self._strategy_to_index(opponets_strategy)
        for i in range(len(caller_strategies)):
            if len(response_indexes) == 0:
                response_indexes.append(i)
                continue

            value = self._get_payoff_value(caller_index, i, opponent_strategy_index)
            current_max =  self._get_payoff_value(caller_index, response_indexes[0], opponent_strategy_index)
            if current_max == value:
                response_indexes.append(i)
                continue

            if current_max < value:
                response_indexes = [i]

        return [caller_strategies[response_index] for response_index in response_indexes]
    
    def get_output(self, first_player_strategy: str, second_player_strategy: str) -> Payoff:
        indexes = self._strategies_to_indexes([[first_player_strategy], [second_player_strategy]])
        return self._payoffs[indexes[0][0]][indexes[1][0]]
    
    def expected_utility(self, mixed_strategy: List[List[float]]):
        """
        Calculate expected utility for both players given their mixed strategies.
        mixed_strategy: A list containing two lists, each representing the mixed strategy
                        probabilities for player 1 and player 2 respectively.
        Returns a list with expected utilities for player 1 and player 2.
        """

        result = [0.0, 0.0]
        for first_player_strategy_index in range(len(self._strategies[self.first_player])):
            for second_player_strategy_index in range(len(self._strategies[self.second_player])):
                propability = (mixed_strategy[self.first_player][first_player_strategy_index] 
                 * mixed_strategy[self.second_player][second_player_strategy_index])
                payoff = self._payoffs[first_player_strategy_index][second_player_strategy_index]
                result[0] += (propability * payoff[0])
                result[1] += (propability * payoff[1])

        return result
    
    def is_mixed_nash_equilibrium(self, mixed_strategy: List[List[float]]) -> bool:
        """
        Check mixed strategy is nash equilibrium with Indifference Principle.
        mixed_strategy: A list containing two lists, each representing the mixed strategy
                        probabilities for player 1 and player 2 respectively.
        """

        # Assume first player's strategy is fixed, check second player's indifference
        for player_index in self.players:
            if not self._is_mixed_nash_equilibrium_for_player(mixed_strategy, player_index):
                return False
        return True
    
    def _is_mixed_nash_equilibrium_for_player(self, mixed_strategy: List[List[float]], player_index: int) -> bool:
        """
        Check mixed strategy is nash equilibrium for given player with Indifference Principle.
        mixed_strategy: A list containing two lists, each representing the mixed strategy
                        probabilities for player 1 and player 2 respectively.
        player_index: The index of the player to check (0 or 1).
        """

        opponent_index = self._get_opponent(player_index)

        # Assume first player's strategy is fixed, check second player's indifference
        expected_utilities_for_each_strategy = []
        for player_strategy_index in range(len(self._strategies[player_index])):
            expected_utility = 0.0
            for opponent_strategy_index in range(len(self._strategies[opponent_index])):
                propability = mixed_strategy[opponent_index][opponent_strategy_index]
                payoff = self._get_payoff_value(player_index, player_strategy_index, opponent_strategy_index)
                expected_utility += (propability * payoff)
            expected_utilities_for_each_strategy.append(expected_utility)

        for i in range(1, len(expected_utilities_for_each_strategy)):
            if abs(expected_utilities_for_each_strategy[i] - expected_utilities_for_each_strategy[0]) > 1e-6:
                return False
            
        return True