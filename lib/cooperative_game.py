def shapley_values(players:list[str], coalitions:list[tuple], worth_of_coalition:list[tuple]) -> dict[str, float]:
    # sort colistions for consistent lookup
    sorted_coalitions = [tuple(sorted(coalition)) for coalition in coalitions]

    permutations:list[tuple] = _permutation(players)
    shapley_values:dict[str, float] = {player: 0.0 for player in players}

    for perm in permutations:
        for player in perm:
            coalition_before = tuple((perm[:perm.index(player)]))
            coalition_with = tuple(sorted(perm[:perm.index(player)+1]))

            index_before = sorted_coalitions.index(tuple(sorted(coalition_before)))
            index_with = sorted_coalitions.index(tuple(sorted(coalition_with)))

            marginal_contribution = worth_of_coalition[index_with] - worth_of_coalition[index_before]
            shapley_values[player] += marginal_contribution / len(permutations)
            
    return shapley_values

def _permutation(elements: list[str]) -> list[tuple]:
    if len(elements) == 0:
        return [()]

    perms = []
    for i in range(len(elements)):
        rest_elements = elements[:i] + elements[i+1:]
        for p in _permutation(rest_elements):
            perms.append((elements[i],) + p)
    return perms

def banzhaf_indexes(players:list[str], coalitions:list[tuple], worth_of_coalition:list[tuple]) -> dict[str, float]:
    # sort colistions for consistent lookup
    sorted_coalitions = [tuple(sorted(coalition)) for coalition in coalitions]

    banzhaf_values:dict[str, float] = {player: 0.0 for player in players}

    for coalition in sorted_coalitions:
        for player in coalition:
            coalition_without = tuple(sorted(set(coalition) - {player}))
            index_without = sorted_coalitions.index(tuple(sorted(coalition_without)))
            index_with = sorted_coalitions.index(tuple(sorted(coalition)))

            marginal_contribution = worth_of_coalition[index_with] - worth_of_coalition[index_without]
            banzhaf_values[player] += marginal_contribution / (2 ** (len(players) - 1))
    
    return banzhaf_values