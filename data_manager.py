import csv
import json

league_filepath = "league_data.json"


def extract_league_data():
    with open(league_filepath) as league_file:
        league_data = json.load(league_file)
    return league_data




def get_players(data):
    players = []
    for game in data:
        for player in game["players"]:
            if player not in players:
                players.append(player)
    return players

def get_game_count(data, player):
    count = 0
    for game in data:
        if player in game["players"]:
            count += 1
    return count

def get_game_counts(data):
    counts = {}
    players = get_players(data)
    for player in players:
        counts[player] = get_game_count(data, player)
    return counts

