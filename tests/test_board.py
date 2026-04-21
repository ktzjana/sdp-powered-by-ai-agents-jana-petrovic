import random

from minesweeper.board import Board


def test_board_be_001_1_s1_constructor_creates_grid_of_correct_size():
    # GIVEN
    rows = 4
    cols = 4
    mines = 2

    # WHEN
    board = Board(rows=rows, cols=cols, mines=mines)

    # THEN
    assert board.rows == 4
    assert board.cols == 4
    assert len(board.grid) == 16
    assert all(cell.revealed is False for cell in board.grid)
    assert all(cell.flagged is False for cell in board.grid)


def test_board_be_001_2_s1_exactly_n_mines_are_placed():
    # GIVEN
    random.seed(42)
    rows, cols, mines = 5, 5, 5

    # WHEN
    board = Board(rows=rows, cols=cols, mines=mines)

    # THEN
    mine_indices = [i for i, cell in enumerate(board.grid) if cell.is_mine]
    assert len(mine_indices) == 5
    assert len(mine_indices) == len(set(mine_indices))
