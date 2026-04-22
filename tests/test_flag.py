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
