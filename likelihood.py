import numpy as np
from scipy.optimize import minimize, Bounds
from random import random
from scipy.stats import beta


def get_win_odds(player_weaknesses, players):
    win_odds = 1
    for player in players:
        weakness = player_weaknesses[player]
        win_odds = win_odds * (1 - weakness)
    return win_odds
    

def get_log_likelihood(player_weaknesses, gamedata, prior_params):
    prior = get_prior(player_weaknesses, prior_params)
    log_likelihood = 0
    for game in gamedata:
        players = game["users"]
        win_odds = get_win_odds(player_weaknesses, players)
        win = "Win" in game["game_outcomes"]
        if win:
            log_likelihood -= np.log(win_odds)
        else:
            log_likelihood -= np.log(1 - win_odds)
    return log_likelihood + prior

def get_prior(player_weaknesses, prior_params):
    surprise = 0
    for weakness in player_weaknesses.values():
        surprise = surprise - np.log(beta.pdf(weakness, prior_params[0], prior_params[1]))
    return surprise

def find_weaknesses(data, players, prior, initial_guess = None):
    if initial_guess == None:
        initial_guess = np.array([0.5 for i, _ in enumerate(players)])
    bounds = Bounds(lb=0.000001, ub=0.99999, keep_feasible=True)
    def convert_to_dict(guess_list):
        guess_dict = {}
        for player, guess in zip(players, guess_list[0]):
            guess_dict[player] = guess
        return guess_dict

    def get_odds(*args):
        player_weaknesses = convert_to_dict(args)
        odds = get_log_likelihood(player_weaknesses, data, prior)
        return odds
    result = minimize(get_odds, initial_guess, bounds=bounds)
    
    ratings = {}
    for player, weakness in zip(players, result.x): 
        ratings[player] = weakness
    return ratings


def find_prior(weaknesses, initial_guess = None):
    def get_surprise(params):
        surprise = 0
        for weakness in weaknesses:
            surprise = surprise - np.log(beta.pdf(weakness, params[0], params[1]))
        return surprise
    if initial_guess == None:
        initial_guess = np.array([2, 2])
    bounds = Bounds(lb=1.0, ub=100.0, keep_feasible=True)
    optimized_prior = minimize(get_surprise, initial_guess, bounds=bounds).x
    return optimized_prior
