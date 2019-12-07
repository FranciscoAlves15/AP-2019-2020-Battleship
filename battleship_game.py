def new_game():
    return {
        'ships': {
            'L': {
                'size': 1,
                'quantity': 4
            },
            'S': {
                'size': 2,
                'quantity': 3
            },
            'F': {
                'size': 3,
                'quantity': 2
            },
            'C': {
                'size': 4,
                'quantity': 1
            },
            'P': {
                'size': 5,
                'quantity': 1
            },
        },
        'players': [],
        'match': None
    }

def has_player(game, name):
    for player in game['players']:
        if player['name'] == name:
            return True
    return False

def add_player(game, name):
    game['players'].append({
        'name': name,
        'matches': 0,
        'wins': 0
    })

def player_in_match(game, name):
    if game['match']['first']['player']['name'] == name:
        return True
    else:
        return game['match']['second']['player']['name'] == name

def remove_player(game, name):
    for i in range(len(game['players'])):
        if game['players'][i]['name'] == name:
            del game['players'][i]
            break

def has_players(game):
    return len(game['players']) != 0

def get_players(game):
    return game['players']

def has_match(game):
    return game['match'] is not None

def start_match(game, player_1_name, player_2_name):
    game['match'] = {
        'first': __create_match_player(game, player_1_name),
        'second': __create_match_player(game, player_2_name)
    }

def place_ship(game, player_name, ship_type, line, column, orientation):
    match_player = __get_match_player(game, player_name)
    ship = {
        'name': ship_type,
        'is_alive': True
    }
    ship_size = game['ships'][ship_type]['size']
    __place_ship(match_player['boards']['ships'], ship, line, column, orientation, ship_size)

def is_valid_position(game, player_name, ship_type, line, column, orientation):
    pass

def is_ship_type_available(game, player_name, ship_type):
    pass

def is_ship_in_position(game, player_name, line, column):
    pass

def remove_ship(game, player_name, line, column):
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

def is_valid_shot(game, line, column):
    pass

def shot(game, player_name, line, column):
    pass

def get_match_state(game):
    pass

def __get_num_ships(game):
    return sum([ship['quantity'] for ship in game['ships'].values()])

def __get_ship_names(game):
    return [ship for ship in game['ships']]

def __get_player(game, name):
    for player in game['players']:
        if player['name'] == name:
            return player

def __get_match_player(game, name):
    for key in game['match']:
        if game['match'][key]['player']['name'] == name:
            return game['match'][key]
    
def __create_match_player(game, player_name):
    return {
        'player': __get_player(game, player_name),
        'ships': {
            'P': [],
            'C': [],
            'F': [],
            'S': [],
            'L': []
        },
        'boards': {
            'ships': [[None for _ in range(10)] for _ in range(10)],
            'shots': [[None for _ in range(10)] for _ in range(10)]
        }
    }

def __get_positions(line, column, orientation, size):
    result = []
    line_step = 0
    column_step = 0
    if orientation == "N":
        line_step = -1 
    elif orientation == "O":
        column_step = -1
    elif orientation == "S":
        line_step = 1
    elif orientation == "E":
        column_step = 1
    for i in range(size):
        result.append({
            'line': line + line_step * i,
            'column': column + column_step * i
        })
    return result

def __place_ship(ship_board, ship, line, column, orientation, size):
    for position in __get_positions(line, column, orientation, size):
        ship_board[position['line']][position['column']] = ship

def __print_ship_board(ship_board):
    for l in range(len(ship_board)):
        for ship in ship_board[l]:
            print(ship['name'] if ship is not None else ".", " ", end="")
        print()

if __name__ == "__main__":
    game = new_game()

    add_player(game, "Bob")
    add_player(game, "Alice")
    start_match(game, "Bob", "Alice")
    place_ship(game, "Alice", "P", 2, 2, "E")
    __print_ship_board(game['match']['second']['boards']['ships'])