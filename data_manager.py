import json
import requests
import sys


LEAGUE_FILEPATH = "league_data.json"
LEAGUE_URL = "https://hanabi-league.com/api/export/games/"

def extract_league_data():
    with open(LEAGUE_FILEPATH) as league_file:
        league_data = json.load(league_file)
    return league_data

def request_league_data():
    result = requests.get(LEAGUE_URL, timeout=10)
    with open(LEAGUE_FILEPATH, "w") as league_file:
        json.dump(result.json(), league_file)

if __name__ == "__main__":
    request_league_data()
