from lib.cooperative_game import shapley_values, banzhaf_indexes

coalitions =         [(), ('O'), ('R'), ('W'), ('O','R'), ('O','W'), ('R','W'), ('O','R','W')]
worth_of_coalition = [ 0,   170,   150,   180,       350,       380,       360,           560]

players = ['O', 'R', 'W']

shapley_vals = shapley_values(players, coalitions, worth_of_coalition)
print("Shapley Values:")
for player, value in shapley_vals.items():
    print(f"{player}: {value}")


banzhaf_indexes = banzhaf_indexes(players, coalitions, worth_of_coalition)
print("\nBanzhaf Indexes:")
for player, index in banzhaf_indexes.items():
    print(f"{player}: {index}")