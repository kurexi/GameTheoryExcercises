from lib.auction import VickeryAuction

# Define auction
agent_evaluations = [2, 4]
available_bids = [0, 1, 2, 3, 4, 5]

auction = VickeryAuction(agent_evaluations, available_bids, tie_breacker=0)

# Utilities when bid truthfully
auction.game().print()