def new_game():
    return {
        'players': [],
        'current': None
    }

def has_player(game, name):
    return name in [player['name'] for player in game['players']]

def add_player(game, name):
    game['players'].append({
        'name': name,
        'wins': 0,
        'losses': 0
    })