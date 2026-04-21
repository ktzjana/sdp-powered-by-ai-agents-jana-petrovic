import random
from dataclasses import dataclass


@dataclass
class Cell:
    revealed: bool = False
    flagged: bool = False
    is_mine: bool = False


class Board:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [Cell() for _ in range(rows * cols)]
        mine_indices = random.sample(range(rows * cols), mines)
        for i in mine_indices:
            self.grid[i].is_mine = True
