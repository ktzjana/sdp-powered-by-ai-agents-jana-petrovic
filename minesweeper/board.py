import random
from dataclasses import dataclass


@dataclass
class Cell:
    revealed: bool = False
    flagged: bool = False
    is_mine: bool = False
    adjacent_count: int = 0


class Board:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [Cell() for _ in range(rows * cols)]
        mine_indices = random.sample(range(rows * cols), mines)
        for i in mine_indices:
            self.grid[i].is_mine = True
        self.compute_adjacent_counts()

    def cell(self, row: int, col: int) -> Cell:
        return self.grid[row * self.cols + col]

    def compute_adjacent_counts(self):
        for row in range(self.rows):
            for col in range(self.cols):
                c = self.cell(row, col)
                if c.is_mine:
                    continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        r, c2 = row + dr, col + dc
                        if (
                            0 <= r < self.rows
                            and 0 <= c2 < self.cols
                            and self.cell(r, c2).is_mine
                        ):
                            count += 1
                self.cell(row, col).adjacent_count = count
