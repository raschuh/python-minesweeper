from random import randint

CONFIGS = {
    "easy": (9, 9, 10),
    "medium": (16, 16, 40),
    "hard": (16, 30, 99)
}

GRID_ADDRESSES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

class MineGrid:
    SYMBOLS = {
        "mine": "*",
        "empty": "0"
    }

    def __init__(self, level="medium"):
        row, col, num_mines = CONFIGS[level]
        self.__grid = [[self.SYMBOLS["empty"] for _ in range(col)] for _ in range(row)]

        for _ in range(num_mines):
            while True:
                _row = randint(0, row - 1)
                _col = randint(0, col - 1)

                if self.__grid[_row][_col] != self.SYMBOLS["mine"]:
                    self.__grid[_row][_col] = self.SYMBOLS["mine"]
                    break

        self.__count_adj_mines()

    def is_empty(self, row, col):
        return self.__grid[row][col] == self.SYMBOLS["empty"]
    
    def is_mine(self, row, col):
        return self.__grid[row][col] == self.SYMBOLS["mine"]
    
    def is_number(self, row, col):
        cell = self.__grid[row][col]
        return cell != self.SYMBOLS["mine"] and cell != self.SYMBOLS["empty"]

    def grid(self):
        return [row[:] for row in self.__grid]

    def __count_adj_mines(self):
        row_len = len(self.__grid)
        col_len = len(self.__grid[0])

        def is_valid_index(i, j, row_len, col_len):
            return i >= 0 and i < row_len and j >= 0 and j < col_len

        counts = [[0 for _ in range(col_len)] for _ in range(row_len)]

        for i in range(row_len):
            for j in range(col_len):
                if self.__grid[i][j] == self.SYMBOLS["mine"]:
                    counts[i][j] = self.SYMBOLS["mine"]
                else:
                    count = sum([1 for x in range(i-1, i+2) for y in range(j-1, j+2) if is_valid_index(x, y, row_len, col_len) and self.__grid[x][y] == self.SYMBOLS["mine"]])
                    counts[i][j] = str(count)

        self.__grid = counts

    def __repr__(self):
        return ",".join(["".join(row) for row in self.__grid])


class StateGrid:
    SYMBOLS = {
        "unopened": "U",
        "opened": "O",
        "flagged": "F"
    }

    def __init__(self, level="medium"):
        row, col, _ = CONFIGS[level]
        self.__grid = [[self.SYMBOLS["unopened"] for _ in range(col)] for _ in range(row)]

    def grid(self):
        return [row[:] for row in self.__grid]

    def is_unopened(self, row, col):
        return self.__grid[row][col] == self.SYMBOLS["unopened"]

    def is_opened(self, row, col):
        return self.__grid[row][col] == self.SYMBOLS["opened"]

    def is_flagged(self, row, col):
        return self.__grid[row][col] == self.SYMBOLS["flagged"]
    
    def count_flags(self):
        return repr(self).count(self.SYMBOLS["flagged"])

    def flag(self, row, col):
        if self.is_opened(row, col):
            return
        if self.is_flagged(row, col):
            self.__grid[row][col] = self.SYMBOLS["unopened"]
        else:
            self.__grid[row][col] = self.SYMBOLS["flagged"]

    def open(self, row, col):
        if self.is_unopened(row, col):
            self.__grid[row][col] = self.SYMBOLS["opened"]

    def __repr__(self):
        return ",".join(["".join(row) for row in self.__grid])


class Game:
    SYMBOLS = {
        "hidden": "#",
        "blank": " ",
        "flag": "F",
        "mine": MineGrid.SYMBOLS["mine"]
    }

    ACTIONS = {
        "open": "O",
        "flag": "F",
        "quit": "Q",
        "reset": "R",
        "resize": "S"
    }

    STATES = {
        "victory": 0,
        "defeat": 1,
        "continue": 2,
        "error": -1
    }

    def __init__(self, level="medium"):
        row, col, num_mines = CONFIGS[level]
        self.__width = col
        self.__height = row
        self.__mine_count = num_mines
        self.__row_addresses = GRID_ADDRESSES[:row]
        self.__col_addresses = GRID_ADDRESSES[:col]
        self.__mine_grid = MineGrid(level)
        self.__state_grid = StateGrid(level)
        self.__state = self.STATES["continue"]

    def update(self, action, row_char, col_char):
        if not self.__validate_location(row_char, col_char):
            self.__state = self.STATES["error"]

        row, col = self.__convert_addresses_to_indexes(row_char, col_char)

        if action == self.ACTIONS["open"]:
            self.__open(row, col)
            if self.__contains_mine(row, col):
                self.__state = self.STATES["defeat"]
            else:
                self.__state = self.STATES["continue"]
        elif action == self.ACTIONS["flag"]:
            self.__flag(row, col)
            self.__state = self.STATES["continue"]
        else:
            self.__state = self.STATES["error"]

        if self.__is_board_cleared():
            self.__state = self.STATES["victory"]
        
        return self.__state
    
    def flags_left(self):
        """Return the count of remaining flags."""
        return self.__mine_count - self.__state_grid.count_flags()
    
    def get_addresses(self):
        return (self.__row_addresses[:], self.__col_addresses[:])
    
    def __open(self, row, col):
        if self.__mine_grid.is_empty(row, col):
            self.__chain_empty_cells(row, col)
        else:
            self.__state_grid.open(row, col)

    def __flag(self, row, col):
        if self.flags_left() > 0:
            self.__state_grid.flag(row, col)

    def __contains_mine(self, row, col):
        return self.__mine_grid.is_mine(row, col)
    
    def __is_board_cleared(self):
        return self.flags_left() == 0 and repr(self.__state_grid).count(StateGrid.SYMBOLS["unopened"]) == 0

    def __validate_location(self, row_char, col_char):
        return row_char in self.__row_addresses and col_char in self.__col_addresses
    
    def __convert_addresses_to_indexes(self, row_char, col_char):
        return (self.__row_addresses.index(row_char), self.__col_addresses.index(col_char))

    def __chain_empty_cells(self, row, col):
        # https://stackoverflow.com/questions/1635641/algorithm-to-search-empty-cells-in-minesweeper/1635655#1635655
        queue = []
        queue.append((row, col))

        while len(queue) > 0:
            y, x = queue.pop(0)
            self.__state_grid.open(y, x)

            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if x + i < 0 or x + i >= self.__width:
                        continue
                    if y + j < 0 or y + j >= self.__height:
                        continue
                    if self.__state_grid.is_unopened(y + j, x + i):
                        if self.__mine_grid.is_empty(y + j, x + i):
                            queue.append((y + j, x + i))
                        elif self.__mine_grid.is_number(y + j, x + i):
                            self.__state_grid.open(y + j, x + i)

    def __reveal(self):
        return ",".join(
            ["".join([c if c != MineGrid.SYMBOLS["empty"] else self.SYMBOLS["blank"] for c in row])
             for row in repr(self.__mine_grid).split(",")])

    def __repr__(self):
        if self.__state == self.STATES["defeat"]:
            return self.__reveal()

        mine_grid = self.__mine_grid.grid()
        state_grid = self.__state_grid.grid()
        str_list = []

        for i in range(self.__height):
            row = []
            for j in range(self.__width):
                state_cell = state_grid[i][j]
                mine_cell = mine_grid[i][j]
                if state_cell == StateGrid.SYMBOLS["unopened"]:
                    row.append(self.SYMBOLS["hidden"])
                elif state_cell == StateGrid.SYMBOLS["opened"]:
                    row.append(mine_cell if mine_cell != MineGrid.SYMBOLS["empty"] else self.SYMBOLS["blank"])
                elif state_cell == StateGrid.SYMBOLS["flagged"]:
                    row.append(self.SYMBOLS["flag"])
            str_list.append("".join(row))

        return ",".join(str_list)
