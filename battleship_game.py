import pickle

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
        'match': None,
        'height': 10,
        'width': 10
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
    return __sort(game['players'], ['name'])

def has_match(game):
    return game['match'] is not None

def start_match(game, player_1_name, player_2_name):
    game['match'] = {
        'first': __create_match_player(game, player_1_name),
        'second': __create_match_player(game, player_2_name),
        'combat': False
    }

def place_ship(game, player_name, ship_type, board_line, board_column, orientation=None):
    match_player = __get_match_player(game, player_name)
    line = __get_line(board_line)
    column = __get_column(board_column)
    ship = {
        'name': ship_type,
        'hits': [],
        'is_alive': True
    }
    ship_size = __get_ship_size(game, ship_type)
    __place_ship(match_player['boards']['ships'], ship, line, column, orientation, ship_size)
    match_player['ships'][ship_type].append(ship)

def is_valid_position(game, player_name, ship_type, board_line, board_column, orientation):
    line = __get_line(board_line)
    column = __get_column(board_column)
    size = __get_ship_size(game, ship_type)
    positions = __get_positions(line, column, orientation, size)
    ships_board = __get_ships_board(game, player_name)
    if __all_positions_in_board(game, positions):
        return not __has_colisions(ships_board, positions)
    else:
        return False

def is_ship_type_available(game, player_name, ship_type):
    max_num_ships = __get_max_ships_of_type(game, ship_type)
    match_player = __get_match_player(game, player_name)
    return len(match_player['ships'][ship_type]) < max_num_ships

def is_ship_in_position(game, player_name, board_line, board_column):
    line = __get_line(board_line)
    column = __get_column(board_column)
    match_player = __get_match_player(game, player_name)
    return __get_ship(match_player, line, column) is not None

def remove_ship(game, player_name, board_line, board_column):
    line = __get_line(board_line)
    column = __get_column(board_column)
    match_player = __get_match_player(game, player_name)
    __remove_ship(match_player, line, column)

def all_ships_placed(game):
    for match_player in __get_match_players(game):
        if len([y for x in match_player['ships'].values() for y in x]) < __get_num_ships(game):
            return False
    return True

def has_combat(game):
    return game['match']['combat']

def start_combat(game):
    game['match']['combat'] = True

def in_match(game, name):
    return name in [match_player['player']['name'] for match_player in __get_match_players(game)]

def withdraw(game, name, second_name=None):
    for match_player in __get_match_players(game):
        if match_player['player']['name'] == name:
            match_player['player']['matches'] += 1
        else:
            match_player['player']['matches'] += 1
            if second_name is None:
                match_player['player']['wins'] += 1
    game['match'] = None

def is_valid_shot(game, board_line, board_column):
    line = __get_line(board_line)
    column = __get_column(board_column)
    return __in_board(game, line, column)

def shot(game, player_name, board_line, board_column):
    result = {
        'ended': False,
        'sunk': False,
        'ship': None
    }
    line = __get_line(board_line)
    column = __get_column(board_column)
    match_player = __get_match_player(game, player_name)
    shots_board = match_player['boards']['shots']
    other_match_player = __get_other_match_player(game, player_name)
    ship = __shoot(game, other_match_player, shots_board, line, column)
    match_player['shots']['all'].append([line, column])
    if ship is not None:
        match_player['shots']['on_ships'].append({
            'ship': ship,
            'shot': [line, column]
        })
        shots_board[line][column] = ship
        result['ship'] = ship
        if not ship['is_alive']:
            result['sunk'] = True
            match_player['shots']['sunk_ships'].append(ship)
        ship_list = [ship for ships in other_match_player['ships'].values() for ship in ships]
        result['ended'] = not any([ship for ship in ship_list if ship['is_alive']])
    else: # hits water
        shots_board[line][column] = {
            'name': 'W'
        }
    __update_state(game)
    return result

def get_match_state(game):
    result = []
    for match_player in __get_match_players(game):
        name = match_player['player']['name']
        total_shots = len(match_player['shots']['all'])
        shots_on_ships = len(match_player['shots']['on_ships'])
        sunk_ships = len(match_player['shots']['sunk_ships'])
        result.append({
            'name': name,
            'total_shots': total_shots,
            'shots_on_ships': shots_on_ships,
            'sunk_ships': sunk_ships
        })
    return result

def save(game, filename):
    with open(filename, "wb") as f:
        pickle.dump(game, f)

def load(filename):
    game = None
    with open(filename, "rb") as f:
        game = pickle.load(f)
    return game

def __get_num_ships(game):
    return sum([ship['quantity'] for ship in game['ships'].values()])

def __get_max_ships_of_type(game, ship_type):
    return game['ships'][ship_type]['quantity']

def __get_ship_names(game):
    return [ship for ship in game['ships']]

def __get_player(game, name):
    for player in game['players']:
        if player['name'] == name:
            return player

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
        'shots': {
            'all': [],
            'on_ships': [],
            'sunk_ships': []
        },
        'boards': {
            'ships': [[None for _ in range(10)] for _ in range(10)],
            'shots': [[None for _ in range(10)] for _ in range(10)]
        }
    }

def __get_match_player(game, name):
    for match_player in __get_match_players(game):
        if match_player['player']['name'] == name:
            return match_player

def __get_other_match_player(game, name):
    for match_player in __get_match_players(game):
        if match_player['player']['name'] != name:
            return match_player

def __get_match_players(game):
    if game['match'] is not None:
        return __sort([game['match'][x] for x in ['first', 'second']], ['player','name'])
    else:
         return []

def __get_ships_board(game, player_name):
    match_player = __get_match_player(game, player_name)
    return match_player['boards']['ships']

def __shoot(game, match_player, shots_board, line, column):
    ship = match_player['boards']['ships'][line][column]
    if ship is not None:
        if [line,column] not in ship['hits']:
            ship['hits'].append([line,column])
        if len(ship['hits']) == __get_ship_size(game, ship['name']):
            ship['is_alive'] = False
    return ship

def __get_ship_size(game, ship_type):
    return game['ships'][ship_type]['size']

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

def __get_ship(match_player, line, column):
    return match_player['boards']['ships'][line][column]

def __remove_ship(match_player, line, column):
    ship = __get_ship(match_player, line, column)
    ship_board = match_player['boards']['ships']
    for l in range(len(ship_board)):
        for c in range(len(ship_board[l])):
            if ship_board[l][c] == ship:
                ship_board[l][c] = None
    match_player['ships'][ship['name']].remove(ship)

def __get_line(line):
    return int(line)-1

def __get_column(column):
    return ord(column.lower()) - ord('a')

def __in_board(game, line, column):
    width = game['width']
    height = game['height']
    return line >= 0 and column >= 0 and line < height and column < width

def __all_positions_in_board(game, positions):
    return not any([x for x in positions if not __in_board(game, x['line'], x['column'])])

def __has_colisions(board, positions):
    ships = []
    height = len(board) -1
    width = len(board[0]) -1
    for position in positions:
        line = position['line']
        column = position['column']
        ships.append(board[line][column])
        ships.append(board[min([max([0,line+1]), width])][column])
        ships.append(board[min([max([0,line-1]), width])][column])
        ships.append(board[line][min([max([0,column+1]), height])])
        ships.append(board[line][min([max([0,column-1]), height])])
        ships.append(board[min([max([0,line-1]), width])][min([max([0,column-1]), height])])
        ships.append(board[min([max([0,line-1]), width])][min([max([0,column+1]), height])])
        ships.append(board[min([max([0,line+1]), width])][min([max([0,column-1]), height])])
        ships.append(board[min([max([0,line+1]), width])][min([max([0,column+1]), height])])
    return any([ship for ship in ships if ship is not None])

def __update_state(game):
    for match_player in __get_match_players(game):
        if len(match_player['shots']['sunk_ships']) == __get_num_ships(game):
            match_player['player']['matches'] += 1
            match_player['player']['wins'] += 1
            other_player = __get_other_match_player(game, match_player['player']['name'])
            other_player['player']['matches'] += 1
            game['match'] = None
            break

def print_ships(game):
    __print_board(game, 'ships')

def print_shots(game):
    __print_board(game, 'shots')

def __print_ship_board(ship_board):
    for l in range(len(ship_board)):
        for ship in ship_board[l]:
            print(f"{ship['name']}" if ship is not None else ".", " ", end="")
        print()

def __print_board(game, board_name):
    height = game['height']
    width = game['width']
    match_players = __get_match_players(game)
    print("\t","\t\t\t".join([player['player']['name'] for player in match_players]))
    print("    A B C D E F G H I J  A B C D E F G H I J")
    for l in range(height):
        line = f"{' ' if l+1 < 10 else ''}{l+1} "
        for match_player in match_players:
            board = match_player['boards'][board_name]
            for ship in board[l]:
                line = f"{line} {ship['name'] if ship is not None else '.'}"
            line = f"{line}\t"
        print(line)

def __sort(dict_list, sort_key, data_type=str):
    for i in range(len(dict_list)):
        for j in range(len(dict_list)-i-1):
            if __get_dict_value(dict_list[j], sort_key) > __get_dict_value(dict_list[j+1], sort_key):
                tmp = dict_list[j]
                dict_list[j] = dict_list[j+1]
                dict_list[j+1] = tmp
    return dict_list

def __get_dict_value(dict, sub_key_list):
    value = dict
    for key in sub_key_list:
        value = value[key]
    return value

if __name__ == "__main__":
    game = new_game()

    add_player(game, "Bob")
    add_player(game, "Alice")
    start_match(game, "Bob", "Alice")

    # place_ship(game, "Alice", "P", "1", "A", "E")
    # place_ship(game, "Alice", "C", "1", "I", "S")
    # place_ship(game, "Alice", "F", "3", "B", "S")
    place_ship(game, "Alice", "F", "10", "H", "E")
    # place_ship(game, "Alice", "S", "3", "F", "S")
    # place_ship(game, "Alice", "S", "8", "F", "S")
    # place_ship(game, "Alice", "S", "10", "C", "O")
    # place_ship(game, "Alice", "L", "8", "B")
    # place_ship(game, "Alice", "L", "6", "E")
    # place_ship(game, "Alice", "L", "6", "G")
    # place_ship(game, "Alice", "L", "7", "I")
    __print_ship_board(__get_ships_board(game, "Alice"))

    # place_ship(game, "Bob", "P", "1", "A", "E")
    # place_ship(game, "Bob", "C", "1", "I", "S")
    # place_ship(game, "Bob", "F", "3", "B", "S")
    # place_ship(game, "Bob", "F", "10", "H", "E")
    # place_ship(game, "Bob", "S", "3", "F", "S")
    # place_ship(game, "Bob", "S", "8", "F", "S")
    # place_ship(game, "Bob", "S", "10", "C", "O")
    # place_ship(game, "Bob", "L", "8", "B")
    # place_ship(game, "Bob", "L", "6", "E")
    # place_ship(game, "Bob", "L", "6", "G")
    # place_ship(game, "Bob", "L", "7", "I")
    # print(all_ships_placed(game))
    # print(in_match(game, "Bob"))
    # print(is_valid_shot(game, "20" , "B"))
    # shot(game, "Alice", "1", "A")
    # shot(game, "Alice", "1", "B")
    # shot(game, "Alice", "1", "C")
    # shot(game, "Alice", "1", "D")
    # shot(game, "Alice", "1", "D")
    # r = shot(game, "Alice", "1", "E")
    # print(get_match_state(game))

    # save(game, "battleship.game")
    # game = load("battleship.game")
    # print(get_match_state(game))