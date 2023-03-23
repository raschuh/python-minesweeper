from game import Game
import ui
import datetime as dt

def main():
    game_level = "easy"
    game = Game(game_level)
    start_time = dt.datetime.now()

    while True:
        ui.display(game, time_elapsed(start_time))
        command = ui.prompt().upper()

        if not command.isalnum():
            continue
        if command[0] == Game.ACTIONS["quit"]:
            break
        if command[0] == Game.ACTIONS["reset"]:
            game = Game(game_level)
            start_time = dt.datetime.now()
        elif command[0] == Game.ACTIONS["resize"] and len(command) == 2:
            game = resize(command[1])
            start_time = dt.datetime.now()
        elif len(command) == 3:
            status = game.update(command[0], command[1], command[2])
            if status == Game.STATES["victory"]:
                ui.display(game, time_elapsed(start_time))
                print("\n😎 - Victory!")
                break
            elif status == Game.STATES["defeat"]:
                ui.display(game, time_elapsed(start_time))
                print("\n😵 - Defeat...")
                break

def resize(size):
    if size == "0":
        game_level = "easy"
    elif size == "1":
        game_level = "medium"
    elif size == "2":
        game_level = "hard"
    return Game(game_level)

def time_elapsed(start_clk):
    return dt.datetime.now() - start_clk

if __name__ == "__main__":
    main()
