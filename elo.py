import numpy as np
nv_elo = 1400

def _get_wr(elo1, elo2):
    return 1 / (1 + 10 ** ((elo2 - elo1) / 400))

def _get_rating(wr, elo):
    return elo - 400 * np.log10(1 / wr - 1)


def get_new_elos(team_elos, k_factors, var_elo, var_k, win):

    player_count = len(team_elos)
    individual_wrs = [_get_wr(elo, var_elo) ** (1.0 / player_count) for elo in team_elos]
    team_wr = np.array(individual_wrs).prod()

    # If the team won, everybody won and variant lost
    if win:
        individual_actuals = [1 for _ in individual_wrs]
        var_actual = 0
    else:
    # If the team lost, the likelihood each player won is between 0 and 1. The variant won.
        individual_actuals = [(wr - team_wr) / (1 - team_wr) for wr in individual_wrs]
        var_actual = 1


    # Use k * (actual - exp) to determine individual rating change
    team_elos_new = [elo + (act - exp) * k \
                     for elo, exp, act, k \
                     in zip(team_elos, individual_wrs, individual_actuals, k_factors)]
    
    
    # Use k * (actual - exp) to determine variant rating change
    var_elo_new = var_elo + (var_actual + team_wr - 1) * var_k
    
    return team_elos_new, var_elo_new


