import numpy as np

from data_manager import extract_league_data
from data_cleaner import make_filter, filter_games
from likelihood import find_weaknesses, find_prior
league_data = extract_league_data()
standard_filter = make_filter(player_count=3, variant=0)
filtered_data = filter_games(league_data, standard_filter)

users = {}
for game in filtered_data:
    for user, user_id in zip(game["users"], game["user_ids"]):
        if user_id not in users:
            users[user_id] = user
game_counts = {}
for user in users.values():
    game_counts[user] = 0
for game in filtered_data:
    for user in game["users"]:
        game_counts[user] = game_counts[user] + 1

players = sorted(users.values(), key=lambda player:game_counts[player], reverse=True)
result = find_weaknesses(filtered_data, players, [3.46, 46.6])

for player in players:
    game_count = game_counts[player]
    if game_count == 1:
        plural = ''
    else:
        plural = 's'
    print(f"{player}: {np.round(100 * result[player], 1)}% with {game_count} game{plural} played.")

prior = find_prior(result.values())
print(prior)