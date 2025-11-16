from lib.printable_strategic_form_game import TwoPlayerStrategicFormGame, PrintableTwoPlayerStrategicFormGame

# Define the Game
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
dominant_game = game.eliminate_weakly_dominated_strategies(print_process=True)
dominant_game.print()

# Pure Nash Equilibria
equilibria = dominant_game.pure_nash_equilibria()
print(f"Pure Nash equilibria for subgame {equilibria}")

equilibria = game.pure_nash_equilibria()
print(f"Pure Nash equilibria for game {equilibria}")