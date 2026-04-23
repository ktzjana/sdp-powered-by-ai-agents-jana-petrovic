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


def test_game_be_002_1_s2_check_win_returns_false_when_safe_cell_unrevealed():
    # GIVEN - a board with 2 mines and 7 safe cells; 1 safe cell still unrevealed
    board = Board(rows=3, cols=3, mines=0)
    board.cell(0, 0).is_mine = True
    board.cell(0, 1).is_mine = True
    board.compute_adjacent_counts()
    game = Game(board)
    # Reveal all safe cells except (2, 2)
    for r in range(3):
        for c in range(3):
            if not board.cell(r, c).is_mine and (r, c) != (2, 2):
                board.cell(r, c).revealed = True

    # WHEN
    result = game.check_win()

    # THEN
    assert result is False


def test_game_be_002_2_s1_game_enters_loss_state_on_mine_hit():
    # GIVEN - a board where cell (1, 1) is a mine
    from minesweeper.game import GameState

    board = Board(rows=3, cols=3, mines=0)
    board.cell(1, 1).is_mine = True
    board.compute_adjacent_counts()
    game = Game(board)

    # WHEN - Game.reveal hits the mine
    game.reveal(1, 1)

    # THEN - game.state == LOSS; subsequent reveal is a no-op
    assert game.state == GameState.LOSS
    game.reveal(0, 0)  # should be rejected
    assert board.cell(0, 0).revealed is False


def test_game_be_002_2_s2_game_enters_win_state_after_check_win_passes():
    # GIVEN - a 2x2 board with 1 mine; reveal all safe cells except the last
    from minesweeper.game import GameState

    board = Board(rows=2, cols=2, mines=0)
    board.cell(0, 0).is_mine = True
    board.compute_adjacent_counts()
    game = Game(board)
    game.reveal(0, 1)
    game.reveal(1, 0)

    # WHEN - the last safe cell is revealed
    game.reveal(1, 1)

    # THEN - game.state == WIN
    assert game.state == GameState.WIN


def test_game_be_002_3_s1_flagged_safe_cell_does_not_satisfy_win_condition():
    # GIVEN - all safe cells except (2, 2) are revealed;
    # (2, 2) is flagged but not revealed
    board = Board(rows=3, cols=3, mines=0)
    board.cell(0, 0).is_mine = True
    board.compute_adjacent_counts()
    game = Game(board)
    for r in range(3):
        for c in range(3):
            if not board.cell(r, c).is_mine and (r, c) != (2, 2):
                board.cell(r, c).revealed = True
    board.cell(2, 2).flagged = True

    # WHEN
    result = game.check_win()

    # THEN - flagged-but-unrevealed cell keeps check_win returning False
    assert result is False


def test_game_fe_002_1_s1_win_message_printed_on_game_completion():
    # GIVEN - a 1x1 board with no mines (revealing the only cell wins immediately)
    import os
    import subprocess
    import sys
    from pathlib import Path

    env = {**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)}

    # WHEN - the player reveals the only safe cell
    result = subprocess.run(
        [
            sys.executable,
            "minesweeper/cli.py",
            "--rows",
            "1",
            "--cols",
            "1",
            "--mines",
            "0",
        ],
        input="r 0 0\n",
        capture_output=True,
        text=True,
        env=env,
    )

    # THEN - "You win!" is printed and process exits cleanly
    assert result.returncode == 0, result.stderr
    assert "You win!" in result.stdout
