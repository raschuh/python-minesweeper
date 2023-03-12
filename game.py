from blessed import Terminal

"""
Prototyping the grid view while experimenting with blessed library
"""

term = Terminal()
grid = [["#"] * 8] * 8

print(term.home + term.clear)
print(term.red + "Hello " + term.green + "World!")

for row in grid:
    print(term.gold + " ---" * len(grid[0]))
    n_row = map(lambda x: term.red + x, row)
    print("| " + (term.gold + " | ").join(n_row) + term.gold + " |")
print(term.gold + " ---" * len(grid[0]))