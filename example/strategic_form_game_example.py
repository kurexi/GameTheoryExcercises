from lib.printable_strategic_form_game import TwoPlayerStrategicFormGame, PrintableTwoPlayerStrategicFormGame

# Pure strategy Game
strategies = [
    ["A", "B", "C", "D" ,"E"],
    ["F", "G", "H", "I" ,"J"]
]

payoffs = [
    [(5,7),(4,1),(4,4),(3,7),(3,4)],
    [(4,4),(5,3),(5,8),(8,1),(3,4)],
    [(1,6),(3,3),(3,5),(2,6),(1,4)],
    [(4,3),(6,1),(8,2),(10,3),(2,3)],
    [(5,3),(5,1),(4,2),(8,3),(3,3)],
]

game = TwoPlayerStrategicFormGame(strategies, payoffs)
game.print()

# Eliminate the dominated strategies
dominant_game = game.eliminate_dominated_strategies(strictly_only=False, print_process=True)
dominant_game.print()

# Pure Nash Equilibria
equilibria = dominant_game.pure_nash_equilibria()
print(f"Pure Nash equilibria for subgame {equilibria}")

equilibria = game.pure_nash_equilibria()
print(f"Pure Nash equilibria for game {equilibria}")


# Mixed strategy Game
strategies = [
    ["T", "B"],
    ["L", "R"]
]

payoffs = [
    [(3,1),(0,4)],
    [(2,3),(1,1)]
]

game2 = TwoPlayerStrategicFormGame(strategies, payoffs)
game2.print()

# No dominated strategies
print(game2.get_weakly_dominant_strategies())

# Expected utilities
mixed_strategies = [[1/3, 2/3],[3/4, 1/4]]
print(game2.expected_utility(mixed_strategies))


# Mixed Nash Equilibria
is_mixed_nash_equilibrium = game2.is_mixed_nash_equilibrium(mixed_strategies)
print(f"Is mixed strategy {mixed_strategies} a mixed Nash equilibrium: {'Yes' if is_mixed_nash_equilibrium else 'No'}")


# Game 3
strategies = [
    ["T", "B"],
    ["L", "R"]
]

payoffs = [
    [(5,2),(3,1)],
    [(4,1),(3,3)]
]

game3 = PrintableTwoPlayerStrategicFormGame(strategies, payoffs)
game3.print()

# dominated strategies
print(game3.get_weakly_dominant_strategies())

# Pure Nash Equilibria
equilibria = game3.pure_nash_equilibria()
print(f"Pure Nash equilibria for game3 {equilibria}")


# Game 4
strategies = [
    ["A", "B", "C", "D", "E", "F"],
    ["G", "H", "I", "J", "K"]
]

payoffs = [
    [(7,7),(1,6),(3,8),(3,10),(5,3)],
    [(11,7),(6,7),(1,9),(3,10),(7,9)],
    [(1,4),(1,4),(1,5),(6,3),(4,2)],
    [(11,1),(5,2),(8,3),(5,4),(8,2)],
    [(7,10),(6,6),(7,11),(3,10),(5,9)],
    [(10,6),(2,6),(7,7),(4,8),(6,7)],
]

game4 = TwoPlayerStrategicFormGame(strategies, payoffs)
game4.print()
subgame = game4.eliminate_dominated_strategies(strictly_only=True, print_process=True)
subgame.print()