# Flag / unflag tests — GAME-BE-003.x scenarios
from minesweeper.board import Board


def test_game_be_003_1_s1_toggle_flag_sets_flagged_true_on_unflagged_cell():
    # GIVEN - cell (1, 4) is unrevealed and not flagged
    board = Board(rows=3, cols=5, mines=0)
    assert board.cell(1, 4).flagged is False
    assert board.cell(1, 4).revealed is False

    # WHEN
    board.toggle_flag(1, 4)

    # THEN
    assert board.cell(1, 4).flagged is True


def test_game_be_003_1_s2_toggle_flag_sets_flagged_false_on_flagged_cell():
    # GIVEN - cell (1, 4) is already flagged
    board = Board(rows=3, cols=5, mines=0)
    board.cell(1, 4).flagged = True

    # WHEN
    board.toggle_flag(1, 4)

    # THEN
    assert board.cell(1, 4).flagged is False


def test_game_be_003_2_s1_toggle_flag_on_revealed_cell_is_noop():
    # GIVEN - cell (2, 2) is already revealed
    board = Board(rows=3, cols=5, mines=0)
    board.cell(2, 2).revealed = True
    board.cell(2, 2).flagged = False

    # WHEN
    board.toggle_flag(2, 2)

    # THEN - flagged state is unchanged and no exception raised
    assert board.cell(2, 2).flagged is False
