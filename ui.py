from blessed import Terminal
import questionary
from game import SYMBOLS

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
        SYMBOLS["mine"]: TERM.black_on_red,
        SYMBOLS["flag"]: TERM.bright_red,
        SYMBOLS["hidden"]: TERM.white
    }

    return colours.get(cell, "") + cell + TERM.normal

def reset():
    print(TERM.home + TERM.clear)

def board(grid_repr):
    str_list = grid_repr.split(",")
    width = len(str_list[0])
    for row in str_list:
        print(TERM.yellow + " ---" * width)
        row = [__colourize(c) for c in row]
        print("| " + (TERM.yellow + " | ").join(row) + TERM.yellow + " |")
    print(TERM.yellow + " ---" * width)

def status(game_stats):
    pass

def prompt():
    questionary.text("> ").ask()
    