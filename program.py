import controllers as cc

def main():
    game = cc.new_game()
    while True:
        line = input()
        if not line:
            exit(0)
        commands = line.split(" ")
        if commands[0] == "RJ":
            name = commands[1]
            if cc.has_player(game, name):
                print("Jogador existente.")
            else:
                cc.add_player(game, name)
                print("Jogador registado com sucesso")
        elif commands[0] == "EJ":
            pass
        elif commands[0] == "LJ":
            pass
        elif commands[0] == "IL":
            pass
        elif commands[0] == "IC":
            pass
        elif commands[0] == "D":
            pass
        elif commands[0] == "CN":
            pass
        elif commands[0] == "RN":
            pass
        elif commands[0] == "T":
            pass
        elif commands[0] == "V":
            pass
        elif commands[0] == "G":
            pass
        elif commands[0] == "L":
            pass

if __name__ == "__main__":
    main()