from data_manager import extract_game_data, get_players, get_game_counts
from likelihood import find_weaknesses
import numpy as np
data = extract_game_data()
three_player_data = [game for game in data if len(game["players"]) == 3]



three_players = get_game_counts(three_player_data)
print(len(three_player_data))
player_names = sorted(three_players, key=lambda player: three_players[player], reverse=True)

print(player_names)
print(three_players)
best_guess = find_weaknesses(three_player_data, three_players.keys())

for player in player_names:
    print(f"{player}: {np.round(100 * best_guess[player], 1)}%")

"""
for i in range(1):
    best_guess = None
    best_odds = None
    guess, odds = sample_weaknesses(three_player_data, three_players)
    if best_odds == None or odds < best_odds:
        best_guess = guess 
        best_odds = odds
        print(best_guess)

    print(best_odds)
"""
