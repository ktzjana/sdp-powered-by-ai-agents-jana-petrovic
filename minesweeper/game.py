from enum import Enum, auto

from minesweeper.board import Board, RevealResult


class GameState(Enum):
    PLAYING = auto()
    WIN = auto()
    LOSS = auto()


class Game:
    def __init__(self, board: Board):
        self.board = board
        self.state = GameState.PLAYING

    def reveal(self, row: int, col: int) -> None:
        if self.state != GameState.PLAYING:
            return
        result = self.board.reveal(row, col)
        if result == RevealResult.MINE_HIT:
            self.state = GameState.LOSS
        elif self.check_win():
            self.state = GameState.WIN

    def check_win(self) -> bool:
        return all(c.revealed for c in self.board.grid if not c.is_mine)

    def flag(self, row: int, col: int) -> None:
        if self.state == GameState.PLAYING:
            self.board.toggle_flag(row, col)
