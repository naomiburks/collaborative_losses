import logging

def filter_games(league_data, game_filter):
    return [game_data for game_data in league_data if game_filter.validate(game_data)]
    
class Filter:
    def __init__(self):
        pass

    def validate(self, data):
        return True
    
class ExactItemFilter(Filter):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        super().__init__()

    def validate(self, data):
        try:
            if data[self.key] == self.value:
                return True
        except KeyError:
            logging.warning("No key %s found!", self.key)
            
        return False

class AndFilter(Filter):
    def __init__(self, filters):
        self.filters = filters
        super().__init__()

    def validate(self, data):
        for data_filter in self.filters:
            if not data_filter.validate(data):
                return False
        return True

def make_filter(player_count, variant):
    player_count_filter = ExactItemFilter("num_players", player_count)
    variant_filter = ExactItemFilter("variant_id", variant)
    return AndFilter([player_count_filter, variant_filter])

