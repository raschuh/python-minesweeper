from blessed import Terminal
import game

def board(term, grid):
    for row in grid:
        print(term.gold + " ---" * len(grid[0]))
        n_row = map(lambda x: term.red + x, row)
        print("| " + (term.gold + " | ").join(n_row) + term.gold + " |")
    print(term.gold + " ---" * len(grid[0]))

def main():
    term = Terminal()
    mine_grid = game.MineGrid("easy")
    print(term.home + term.clear)
    board(term, mine_grid.grid())
    print(repr(mine_grid))
    

if __name__ == "__main__":
    main()
