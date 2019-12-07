def new_game():
    return {
        'players': [],
        'ships': [],
        'match': None
    }

def has_player(game, name):
    pass

def add_player(game, name):
    pass

def has_current_match(game):
    pass

def player_in_current_match(game, name):
    pass

def remove_player(game, name):
    pass

def has_players(game):
    pass

def get_players(game):
    pass

def has_match(game):
    pass

def start_match(game, player_1_name, player_2_name):
    pass

def all_ships_placed(game):
    pass

def has_combat(game):
    pass

def start_combat(game):
    pass

def in_match(game, name):
    pass

def withdraw(game, first, second_name=None):
    pass

def is_valid_position(game, player_name, ship_type, line, column, orientation):
    pass

def is_ship_type_available(game, player_name, ship_type):
    pass

def place_ship(game, player_name, ship_type, line, column, orientation):
    pass

def is_ship_in_position(game, player_name, line, column):
    pass

def remove_ship(game, player_name, line, column):
    pass

def is_valid_shot(game, line, column):
    pass

def shot(game, player_name, line, column):
    pass

def get_current_match_state(game):
    pass