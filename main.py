from game import Game
import ui

def main():
    game_level = "easy"
    game = Game(game_level)

    while True:
        ui.reset()
        ui.board(repr(game))
        command = ui.prompt().upper()

        if command[0] == Game.ACTIONS["quit"]:
            break
        if command[0] == Game.ACTIONS["reset"]:
            game = Game(game_level)
        else:
            status = game.update(command[0], int(command[1]), int(command[2]))
            if status == Game.STATES["gameover"]:
                ui.reset()
                ui.board(game.reveal())
                break


if __name__ == "__main__":
    main()
