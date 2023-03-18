from random import randint

CONFIGS = {
    "easy": (9, 9, 10),
    "medium": (16, 16, 40),
    "hard": (16, 30, 99)
}

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
        return self.contains_mine(row, col)
    
    def is_number(self, row, col):
        cell = self.__grid[row][col]
        return cell != self.SYMBOLS["mine"] and cell != self.SYMBOLS["empty"]

    def contains_mine(self, row, col):
        return self.__grid[row][col] == self.SYMBOLS["mine"]

    def grid(self):
        return [row[:] for row in self.__grid]

    def __count_adj_mines(self):
        row_len = len(self.__grid)
        col_len = len(self.__grid[0])

        for i in range(row_len):
            for j in range(col_len):
                if self.__grid[i][j] == self.SYMBOLS["mine"]:
                    continue

                count = 0
                if i - 1 >= 0 and j - 1 >= 0 and self.__grid[i - 1][j - 1] == self.SYMBOLS["mine"]:
                    count += 1
                if i - 1 >= 0 and self.__grid[i - 1][j] == self.SYMBOLS["mine"]:
                    count += 1
                if i - 1 >= 0 and j + 1 < col_len and self.__grid[i - 1][j + 1] == self.SYMBOLS["mine"]:
                    count += 1
                if j - 1 >= 0 and self.__grid[i][j - 1] == self.SYMBOLS["mine"]:
                    count += 1
                if j + 1 < col_len and self.__grid[i][j + 1] == self.SYMBOLS["mine"]:
                    count += 1
                if i + 1 < row_len and j - 1 >= 0 and self.__grid[i + 1][j - 1] == self.SYMBOLS["mine"]:
                    count += 1
                if i + 1 < row_len and self.__grid[i + 1][j] == self.SYMBOLS["mine"]:
                    count += 1
                if i + 1 < row_len and j + 1 < col_len and self.__grid[i + 1][j + 1] == self.SYMBOLS["mine"]:
                    count += 1

                self.__grid[i][j] = str(count)

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

    def flag(self, row, col):
        if not self.is_unopened(row, col):
            return False

        self.__grid[row][col] = self.SYMBOLS["flagged"]
        return True

    def open(self, row, col):
        if not self.is_unopened(row, col):
            return False

        self.__grid[row][col] = self.SYMBOLS["opened"]
        return True

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
        "reset": "R"
    }

    STATES = {
        "gameover": 0,
        "continue": 1,
        "error": -1
    }

    def __init__(self, level="medium"):
        row, col, num_mines = CONFIGS[level]
        self.width = col
        self.height = row
        self.mine_count = num_mines
        self.__mine_grid = MineGrid(level)
        self.__state_grid = StateGrid(level)

    def open(self, row, col):
        if self.__mine_grid.is_empty(row, col):
            self.__chain_empty_cells(row, col)
            return True
        return self.__state_grid.open(row, col)

    def flag(self, row, col):
        return self.__state_grid.flag(row, col)

    def contains_mine(self, row, col):
        return self.__mine_grid.contains_mine(row, col)

    def update(self, action, row, col):
        if action == self.ACTIONS["open"]:
            if self.open(row, col):
                return self.STATES["gameover"] if self.contains_mine(row, col) else self.STATES["continue"]
            return self.STATES["error"]
        if action == self.ACTIONS["flag"]:
            return self.STATES["continue"] if self.flag(row, col) else self.STATES["error"]
        return self.STATES["error"]

    def reveal(self):
        return ",".join(
            ["".join([c if c != MineGrid.SYMBOLS["empty"] else self.SYMBOLS["blank"] for c in row])
             for row in repr(self.__mine_grid).split(",")])
    
    def __chain_empty_cells(self, row, col):
        # https://stackoverflow.com/questions/1635641/algorithm-to-search-empty-cells-in-minesweeper/1635655#1635655
        queue = []
        queue.append((row, col))

        while len(queue) > 0:
            y, x = queue.pop(0)
            self.__state_grid.open(y, x)
            
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if x + i < 0 or x + i >= self.width:
                        continue
                    if y + j < 0 or y + j >= self.height:
                        continue
                    if self.__state_grid.is_unopened(y + j, x + i):
                        if self.__mine_grid.is_empty(y + j, x + i):
                            queue.append((y + j, x + i))
                        elif self.__mine_grid.is_number(y + j, x + i):
                            self.__state_grid.open(y + j, x + i)

    def __repr__(self):
        mine_grid = self.__mine_grid.grid()
        state_grid = self.__state_grid.grid()
        str_list = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
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
