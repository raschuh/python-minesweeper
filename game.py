from random import randint

CONFIGS = {
    "easy": (9, 9, 10),
    "medium": (16, 16, 40),
    "hard": (16, 30, 99)
}

SYMBOLS = {
    "mine": "*",
    "flag": "F",
    "opened": "O",
    "unopened": "U",
    "hidden": "#",
    "blank": " "
}


class MineGrid:
    def __init__(self, level="medium"):
        row, col, num_mines = CONFIGS[level]
        self.__grid = [[SYMBOLS["blank"] for _ in range(col)] for _ in range(row)]

        for _ in range(num_mines):
            while True:
                _row = randint(0, row - 1)
                _col = randint(0, col - 1)

                if self.__grid[_row][_col] != SYMBOLS["mine"]:
                    self.__grid[_row][_col] = SYMBOLS["mine"]
                    break

        self.__count_adj_mines()

    def contains_mine(self, row, col):
        return self.__grid[row][col] == SYMBOLS["mine"]

    def grid(self):
        return [row[:] for row in self.__grid]

    def __count_adj_mines(self):
        row_len = len(self.__grid)
        col_len = len(self.__grid[0])

        for i in range(row_len):
            for j in range(col_len):
                if self.__grid[i][j] == SYMBOLS["mine"]:
                    continue

                count = 0
                if i - 1 >= 0 and j - 1 >= 0 and self.__grid[i - 1][j - 1] == SYMBOLS["mine"]:
                    count += 1
                if i - 1 >= 0 and self.__grid[i - 1][j] == SYMBOLS["mine"]:
                    count += 1
                if i - 1 >= 0 and j + 1 < col_len and self.__grid[i - 1][j + 1] == SYMBOLS["mine"]:
                    count += 1
                if j - 1 >= 0 and self.__grid[i][j - 1] == SYMBOLS["mine"]:
                    count += 1
                if j + 1 < col_len and self.__grid[i][j + 1] == SYMBOLS["mine"]:
                    count += 1
                if i + 1 < row_len and j - 1 >= 0 and self.__grid[i + 1][j - 1] == SYMBOLS["mine"]:
                    count += 1
                if i + 1 < row_len and self.__grid[i + 1][j] == SYMBOLS["mine"]:
                    count += 1
                if i + 1 < row_len and j + 1 < col_len and self.__grid[i + 1][j + 1] == SYMBOLS["mine"]:
                    count += 1

                self.__grid[i][j] = str(count)

    def __repr__(self):
        return ",".join(["".join(row) for row in self.__grid])


class StateGrid:
    def __init__(self, level="medium"):
        row, col, _ = CONFIGS[level]
        self.__grid = [[SYMBOLS["unopened"] for _ in range(col)] for _ in range(row)]

    def grid(self):
        return [row[:] for row in self.__grid]

    def is_unopened(self, row, col):
        return self.__grid[row][col] == SYMBOLS["unopened"]

    def is_opened(self, row, col):
        return self.__grid[row][col] == SYMBOLS["opened"]

    def is_flagged(self, row, col):
        return self.__grid[row][col] == SYMBOLS["flag"]

    def flag(self, row, col):
        if not self.is_unopened(row, col):
            return False

        self.__grid[row][col] = SYMBOLS["flag"]
        return True

    def open(self, row, col):
        if not self.is_unopened(row, col):
            return False

        self.__grid[row][col] = SYMBOLS["opened"]
        return True

    def __repr__(self):
        return ",".join(["".join(row) for row in self.__grid])


class Game:
    def __init__(self, level="medium"):
        row, col, num_mines = CONFIGS[level]
        self.width = col
        self.height = row
        self.mine_count = num_mines
        self.__mine_grid = MineGrid(level)
        self.__state_grid = StateGrid(level)

    def open(self, row, col):
        return self.__state_grid.open(row, col)

    def flag(self, row, col):
        return self.__state_grid.flag(row, col)

    def contains_mine(self, row, col):
        return self.__mine_grid.contains_mine(row, col)

    def update(self, action, row, col):
        if action == SYMBOLS["opened"]:
            if self.open(row, col):
                return 0 if self.contains_mine(row, col) else 1
            else:
                return -1
        elif action == SYMBOLS["flag"]:
            return 1 if self.flag(row, col) else -1
        else:
            return -1

    def reveal(self):
        return ",".join(
            ["".join([c if c != "0" else SYMBOLS["blank"] for c in row])
             for row in repr(self.__mine_grid).split(",")])

    def __repr__(self):
        mine_grid = self.__mine_grid.grid()
        state_grid = self.__state_grid.grid()
        str_list = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                state_cell = state_grid[i][j]
                mine_cell = mine_grid[i][j]
                if state_cell == SYMBOLS["unopened"]:
                    row.append(SYMBOLS["hidden"])
                elif state_cell == SYMBOLS["opened"]:
                    row.append(mine_cell if mine_cell != "0" else SYMBOLS["blank"])
                elif state_cell == SYMBOLS["flag"]:
                    row.append(SYMBOLS["flag"])
            str_list.append("".join(row))
        return ",".join(str_list)
