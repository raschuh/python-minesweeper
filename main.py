from game import Game
import ui
import datetime as dt

START_TIME = dt.datetime.now()

def main():
    game_level = "easy"
    game = Game(game_level)

    while True:
        ui.display(game, get_timedelta())
        command = ui.prompt().upper()

        if not command.isalnum():
            continue
        if command[0] == Game.ACTIONS["quit"]:
            break
        if command[0] == Game.ACTIONS["reset"]:
            game = Game(game_level)
        elif command[0] == Game.ACTIONS["resize"] and len(command) == 2:
            game = resize(command[1])
        elif len(command) == 3:
            status = game.update(command[0], command[1], command[2])
            if status == Game.STATES["victory"]:
                ui.display(game, get_timedelta())
                print("😎")
                break
            elif status == Game.STATES["defeat"]:
                ui.display(game, get_timedelta())
                print("😵")
                break

def resize(size):
    if size == "0":
        game_level = "easy"
    elif size == "1":
        game_level = "medium"
    elif size == "2":
        game_level = "hard"
    return Game(game_level)

def get_timedelta():
    return dt.datetime.now() - START_TIME

if __name__ == "__main__":
    main()
