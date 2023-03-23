from blessed import Terminal
import questionary
from game import Game

TERM = Terminal()

def __colourize(cell):
    colours = {
        "1": TERM.cyan,
        "2": TERM.green,
        "3": TERM.bright_red,
        "4": TERM.magenta,
        "5": TERM.cyan,
        "6": TERM.green,
        "7": TERM.bright_red,
        "8": TERM.magenta,
        Game.SYMBOLS["mine"]: TERM.black_on_red,
        Game.SYMBOLS["flag"]: TERM.bright_red,
        Game.SYMBOLS["hidden"]: TERM.white
    }

    return colours.get(cell, "") + cell + TERM.normal

def reset():
    print(TERM.home + TERM.clear)

def board(game):
    str_list = repr(game).split(",")
    height = len(str_list)
    width = len(str_list[0])
    row_addrs, col_addr = game.get_addresses()
    print(TERM.cyan + "    " + "   ".join(col_addr))
    for i in range(height):
        print(TERM.yellow + "   ---" + " ---" * (width - 1))
        row = [__colourize(c) for c in str_list[i]]
        print(TERM.cyan + row_addrs[i] + TERM.yellow + " | " + (TERM.yellow + " | ").join(row) + TERM.yellow + " |")
    print(TERM.yellow + "   ---" + " ---" * (width - 1))

def status(game, time_delta):
    print()
    print(f"Flags Left: {game.flags_left()}")
    print(f"Elasped Time: {int(time_delta.total_seconds())}s")

def display(game, time_delta):
    reset()
    board(game)
    status(game, time_delta)

def prompt():
    return questionary.text("> ").ask()
    