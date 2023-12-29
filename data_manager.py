import json

league_filepath = "league_data.json"


def extract_league_data():
    with open(league_filepath) as league_file:
        league_data = json.load(league_file)
    return league_data
