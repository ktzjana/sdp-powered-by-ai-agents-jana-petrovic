from dataclasses import dataclass


@dataclass
class Cell:
    revealed: bool = False
    flagged: bool = False


class Board:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [Cell() for _ in range(rows * cols)]
