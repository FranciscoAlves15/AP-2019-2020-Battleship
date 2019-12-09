import battleship_game as bg

def main():
    filename = "battleship.game"
    game = bg.new_game()
    while True:
        line = input()
        if not line:
            exit(0)
        commands = line.split(" ")
        if commands[0] == "RJ":
            commandRJ(commands, game)
        elif commands[0] == "EJ":
            commandEJ(commands, game)
        elif commands[0] == "LJ":
            commandLJ(commands, game)
        elif commands[0] == "IJ":
            commandIJ(commands, game)
        elif commands[0] == "IC":
            commandIC(commands, game)
        elif commands[0] == "D":
            commandD(commands, game)
        elif commands[0] == "CN":
            commandCN(commands, game)
        elif commands[0] == "RN":
            commandRN(commands, game)
        elif commands[0] == "T":
            commandT(commands, game)
        elif commands[0] == "V":
            commandV(commands, game)
        elif commands[0] == "G":
            commandG(commands, game, filename)
        elif commands[0] == "L":
            game = commandL(commands, filename)
        # Extra commands
        elif commands[0] == "PN":
            commandPN(commands, game)
        elif commands[0] == "PT":
            commandPT(commands, game)
        else:
            print("Instrução inválida.")

def commandRJ(commands, game):
    name = commands[1]
    if bg.has_player(game, name):
        print("Jogador existente.")
    else:
        bg.add_player(game, name)
        print("Jogador registado com sucesso")

def commandEJ(commands, game):
    name = commands[1]
    if not bg.has_player(game, name):
        print("Jogador não existente.")
    elif bg.in_match(game, name):
        print("Jogador participa no jogo em curso.")
    else:
        bg.remove_player(game, name)
        print("Jogador removido com sucesso.")   

def commandLJ(commands, game):
    if not bg.has_players(game):
        print("Não existem jogadores registados.")
    else:
        for player in bg.get_players(game):
            print(f"{player['name']} {player['matches']} {player['wins']}")

def commandIJ(commands, game):
    player_1_name = commands[1]
    player_2_name = commands[2]
    if bg.has_match(game):
        print("Existe um jogo em curso.")
    elif (not bg.has_player(game, player_1_name)) or (not bg.has_player(game, player_2_name)):
        print("Jogadores não registados.")
    else:
        bg.start_match(game, player_1_name, player_2_name)
        print("Jogo iniciado com sucesso.")

def commandIC(commands, game):
    if not bg.has_match(game):
        print("Não existe jogo em curso.")
    elif not bg.all_ships_placed(game):
        print("Navios não colocados.")
    else:
        if not bg.has_combat(game):
            bg.start_combat(game)
        print("Combate iniciado.")

def commandD(commands, game):
    player_1_name = commands[1]
    player_2_name = commands[2] if len(commands==3) else None
    if not bg.has_match(game):
        print("Não existe jogo em curso.")
    elif (not bg.in_match(game, player_1_name)) or (not bg.in_match(game, player_2_name)):
        print("Jogador não participa no jogo em curso.")
    else:
        bg.withdraw(game, player_1_name, player_2_name)
        print("Desistência com sucesso. Jogo terminado.")

def commandCN(commands, game):
    player_name = commands[1]
    ship_type = commands[2]
    line = commands[3]
    column = commands[4]
    orientation = commands[5] if len(commands) == 6 else None
    if not bg.has_match(game):
        print("Não existe jogo em curso.")
    elif not bg.in_match(game, player_name):
        print("Jogador não participa no jogo em curso.")
    elif not bg.is_valid_position(game, player_name, ship_type, line, column, orientation):
        print("Posição irregular.")
    elif not bg.is_ship_type_available(game, player_name, ship_type):
        print("Não tem mais navios dessa tipologia disponíveis.")
    else:
        bg.place_ship(game, player_name, ship_type, line, column, orientation)
        print("Navio colocado com sucesso.")
        
def commandRN(commands, game):
    player_name = commands[1]
    line = commands[2]
    column = commands[3]
    if not bg.has_match(game):
        print("Não existe jogo em curso")
    elif not bg.in_match(game, player_name):
        print("Jogador não participa no jogo em curso.")
    elif not bg.is_ship_in_position(game, player_name, line, column):
        print("Não existe navio na posição.")
    else:
        bg.remove_ship(game, player_name, line, column)
        print("Navio removido com sucesso.")

def commandT(commands, game):
    player_name = commands[1]
    line = commands[2]
    column = commands[3]
    if not bg.has_match(game):
        print("Não existe jogo em curso")
    elif not bg.in_match(game, player_name):
        print("Jogador não participa no jogo em curso.")
    elif not bg.is_valid_shot(game, line, column):
        print("Posição irregular.")
    else:
        shot = bg.shot(game, player_name, line, column)
        if shot['ended']:
            print(f"Navio {shot['ship']['name']} afundado. Jogo terminado.")
        elif shot['sunk']:
            print(f"Navio {shot['ship']['name']} afundado.")
        elif shot['ship'] is not None:
            print("Tiro em navio.")
        else:
            print("Tiro na água.")

def commandV(commands, game):
    if not bg.has_match(game):
        print("Não existe jogo em curso.")
    elif not bg.has_combat(game):
        print("Jogo em curso sem combate iniciado.")
    else:
        result = bg.get_match_state(game)
        for e in result:
            print(f"{e['name']} {e['total_shots']} {e['shots_on_ships']} {e['sunk_ships']}")

def commandG(commands, game, filename):
    try:
        bg.save(game, filename)
        print("Jogo gravado.")
    except Exception as e:
        print("Ocorreu um erro na gravação.")

def commandL(commands, filename):
    try:
        game = bg.load(filename)
        print("Jogo carregado.")
    except Exception as e:
        print("Ocorreu um erro no carregamento.")

def commandPN(commands, game):
    bg.print_ships(game)

def commandPT(commands, game):
    bg.print_shots(game)

if __name__ == "__main__":
    main()
