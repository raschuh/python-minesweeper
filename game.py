from random import randint

CONFIGS = {
    "easy": (9, 9, 10),
    "medium": (16, 16, 40),
    "hard": (16, 30, 99)
}

class MineGrid:
    def __init__(self, level="medium"):
        row, col, num_mines = CONFIGS[level]
        self.__grid = [[" " for _ in range(col)] for _ in range(row)]
        
        for _ in range(num_mines):
            while True:
                _row = randint(0, row - 1)
                _col = randint(0, col - 1)
                
                if self.__grid[_row][_col] != "M":
                    self.__grid[_row][_col] = "M"
                    break

        self.__count_adj_mines()

    def contains_mine(self, row, col):
        return self.__grid[row][col] == "M"
    
    def grid(self):
        copy_grid = []
        for row in self.__grid:
            copy_grid.append(row[:])
        return copy_grid
    
    def __count_adj_mines(self):
        row_len = len(self.__grid)
        col_len = len(self.__grid[0])

        for i in range(row_len):
            for j in range(col_len):
                if self.__grid[i][j] == "M":
                    continue

                count = 0
                if i - 1 >= 0 and j - 1 >= 0 and self.__grid[i - 1][j - 1] == "M":
                    count += 1
                if i - 1 >= 0 and self.__grid[i - 1][j] == "M":
                    count += 1
                if i - 1 >= 0 and j + 1 < col_len and self.__grid[i - 1][j + 1] == "M":
                    count += 1
                if j - 1 >= 0 and self.__grid[i][j - 1] == "M":
                    count += 1
                if j + 1 < col_len and self.__grid[i][j + 1] == "M":
                    count += 1
                if i + 1 < row_len and j - 1 >= 0 and self.__grid[i + 1][j - 1] == "M":
                    count += 1
                if i + 1 < row_len and self.__grid[i + 1][j] == "M":
                    count += 1
                if i + 1 < row_len and j + 1 < col_len and self.__grid[i + 1][j + 1] == "M":
                    count += 1

                self.__grid[i][j] = str(count)

    def __repr__(self):
        row_list = ["".join(row) for row in self.__grid]
        return ",".join(row_list)


class StateGrid:
    def __init__(self, level="medium"):
        row, col, _ = CONFIGS[level]
        self.__grid = [["U" for _ in range(col)] for _ in range(row)]

    def grid(self):
        copy_grid = []
        for row in self.__grid:
            copy_grid.append(row[:])
        return copy_grid
    
    def is_unopened(self, row, col):
        return self.__grid[row][col] == "U"
    
    def is_opened(self, row, col):
        return self.__grid[row][col] == "O"
    
    def is_flagged(self, row, col):
        return self.__grid[row][col] == "F"
    
    def flag(self, row, col):
        if not self.is_unopened(row, col):
            return False
        
        self.__grid[row][col] = "F"
        return True
    
    def open(self, row, col):
        if not self.is_unopened(row, col):
            return False
        
        self.__grid[row][col] = "O"
        return True
    
    def __repr__(self):
        row_list = ["".join(row) for row in self.__grid]
        return ",".join(row_list)
    
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
        if action == "O":
            if self.open(row, col):
                return 0 if self.contains_mine(row, col) else 1
            else:
                return -1
        elif action == "F":
            return 1 if self.flag(row, col) else -1
        else:
            return -1

    def reveal(self):
        pass

    def __repr__(self):
        pass