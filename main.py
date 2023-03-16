import game
import ui

def main():
    _game = game.Game("easy")
    _game.open(1, 3)
    _game.open(5, 6)
    ui.reset()
    ui.board(_game.reveal())
    print(repr(_game._Game__mine_grid))
    print(_game.reveal())
    print(repr(_game))


if __name__ == "__main__":
    main()
