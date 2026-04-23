# Win/loss detection tests — GAME-BE-002.x scenarios
from minesweeper.board import Board
from minesweeper.game import Game


def test_game_be_002_1_s1_check_win_returns_true_when_all_safe_cells_revealed():
    # GIVEN - a board with 2 mines and 7 safe cells, all safe cells revealed
    board = Board(rows=3, cols=3, mines=0)
    board.cell(0, 0).is_mine = True
    board.cell(0, 1).is_mine = True
    board.compute_adjacent_counts()
    game = Game(board)
    for r in range(3):
        for c in range(3):
            if not board.cell(r, c).is_mine:
                board.cell(r, c).revealed = True

    # WHEN
    result = game.check_win()

    # THEN
    assert result is True
