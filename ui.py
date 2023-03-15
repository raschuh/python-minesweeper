from blessed import Terminal
from game import Game

def board(term: Terminal, game: Game):
    for row in game.grid:
        print(term.gold + " ---" * len(game.grid[0]))
        n_row = map(lambda x: term.red + x, row)
        print("| " + (term.gold + " | ").join(n_row) + term.gold + " |")
    print(term.gold + " ---" * len(game.grid[0]))

