from lib.auction import VickeryAuction, vickery_auction_expected_utilities, first_price_sealed_bid_auction_expected_utilities
from typing import List, Tuple

# Define auction
agent_evaluations = [2, 4]
available_bids = [0, 1, 2, 3, 4, 5]

auction = VickeryAuction(agent_evaluations, available_bids, tie_breacker=0)
auction.print()

# Utilities when bid truthfully
# sub game strategies [[agent_evaluations[0]],[agent_evaluations[1]]]
outcome = auction.outcome(agent_evaluations)
print("Outcome of truthful bids")
print(outcome)


# Is evey-free
is_envy_free = auction.is_envy_free(agent_evaluations)
print(f"Is outcome of truthful bids Envy-free: {'Yes' if is_envy_free else 'No'}")


# Pure Nash Equilibria
equilibria = auction.game().pure_nash_equilibria()
print(f"Pure Nash equilibria:\n {equilibria}")


# Envy-free Pure Nash Equilibria
envy_free_equilibria = [entry for entry in equilibria if auction.is_envy_free(list(entry))]
print(f"Envy-free Pure Nash equilibria:\n {envy_free_equilibria}")


# Check if nash equilibria change with different tie-breaking rule
auction_with_different_tie_breaking = VickeryAuction(agent_evaluations, available_bids, tie_breacker=1)
equilibria_with_different_tie_breaking = auction_with_different_tie_breaking.game().pure_nash_equilibria()

def is_outcome_set_a_in_b(set_a: List[Tuple], set_b: List[Tuple]) -> bool:    
    for ea in set_a:
        contains = False
        for eb in set_b:
            if ea[0] == eb[0] and ea[1] == eb[1]:
                contains = True
                break
        if not contains:
            print(f"Missing: {ea}")
            return False
    return True
        
def is_outcome_set_a_equal_to_b(set_a: List[Tuple], set_b: List[Tuple]) -> bool:
    return (is_outcome_set_a_in_b(set_a, set_b) and is_outcome_set_a_in_b(set_b, set_a))

is_different = not is_outcome_set_a_equal_to_b(equilibria, equilibria_with_different_tie_breaking)
print(f"Is equilibria different with diffrent tie breaking: {'Yes' if is_different else 'No'}")


# Check if envy-free outcome change with different tie-breaking rule
envy_free_equilibria_diff_tie = [entry for entry in equilibria_with_different_tie_breaking if auction_with_different_tie_breaking.is_envy_free(list(entry))]
is_different = not is_outcome_set_a_equal_to_b(envy_free_equilibria, envy_free_equilibria_diff_tie)
print(f"Is envy-free equilibria different with diffrent tie breaking: {'Yes' if is_different else 'No'}")


# expected utilities

agent_evaluation = 7
winning_bid_probabilites = {
    2: 0,
    3: 0.1,
    4: 0.25,
    5: 0.35,
    6: 0.40,
    7: 0.65,
    8: 0.85,
    9: 0.95,
    10: 1
}

bids = list(winning_bid_probabilites.keys())
probabilities = list(winning_bid_probabilites.values())

# First-price sealed-bid auction expected utilities
expected_utilities = first_price_sealed_bid_auction_expected_utilities(agent_evaluation, bids, probabilities)
print(f"First-price sealed-bid auction expected utilities: {expected_utilities}")

# Vickery auction expected utilities
expected_utilities = vickery_auction_expected_utilities(agent_evaluation, bids, probabilities)
print(f"Vickery auction expected utilities: {expected_utilities}")