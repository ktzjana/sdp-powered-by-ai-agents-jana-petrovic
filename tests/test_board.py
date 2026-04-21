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
