# Flag / unflag tests — GAME-BE-003.x scenarios
from pathlib import Path

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


def test_game_story_003_s1_flag_unrevealed_cell():
    # GIVEN - cell (1, 4) is unrevealed and not flagged
    from minesweeper.game import Game
    from minesweeper.renderer import BoardRenderer

    board = Board(rows=3, cols=5, mines=0)
    game = Game(board)
    assert board.cell(1, 4).flagged is False
    assert board.cell(1, 4).revealed is False

    # WHEN - the player dispatches flag command f 1 4
    game.flag(1, 4)

    # THEN - cell is flagged and board renders flag marker at (1, 4)
    assert board.cell(1, 4).flagged is True
    output = BoardRenderer.render(board)
    assert output.strip().splitlines()[1].split()[4] == "F"


def test_game_story_003_s2_unflag_flagged_cell_toggle():
    # GIVEN - cell (1, 4) is already flagged
    from minesweeper.game import Game
    from minesweeper.renderer import BoardRenderer

    board = Board(rows=3, cols=5, mines=0)
    game = Game(board)
    game.flag(1, 4)
    assert board.cell(1, 4).flagged is True

    # WHEN - the player dispatches flag command f 1 4 again
    game.flag(1, 4)

    # THEN - cell is unflagged and board renders hidden marker at (1, 4)
    assert board.cell(1, 4).flagged is False
    output = BoardRenderer.render(board)
    assert output.strip().splitlines()[1].split()[4] == "."


def test_game_story_003_s3_flag_on_revealed_cell_is_ignored():
    # GIVEN - cell (2, 2) has already been revealed
    from minesweeper.game import Game, GameState

    board = Board(rows=3, cols=5, mines=0)
    game = Game(board)
    board.cell(2, 2).revealed = True

    # WHEN - the player dispatches flag command f 2 2
    game.flag(2, 2)

    # THEN - board state is unchanged, no error, game continues
    assert board.cell(2, 2).flagged is False
    assert game.state == GameState.PLAYING


def test_game_story_003_s4_e2e_flag_cell_and_verify_board_display():
    # GIVEN - the game is started with --seed 42
    import os
    import subprocess
    import sys

    env = {**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)}

    # WHEN - the player enters f 0 0 then q
    result = subprocess.run(
        [sys.executable, "minesweeper/cli.py", "--seed", "42"],
        input="f 0 0\nq\n",
        capture_output=True,
        text=True,
        env=env,
    )

    # THEN - stdout contains F at (0,0), process exits with code 0
    assert result.returncode == 0, f"non-zero exit: {result.stderr}"
    assert "F" in result.stdout
    # The second board render (after f 0 0) should show F at position (0, 0)
    lines = result.stdout.strip().splitlines()
    # Find the first line that starts with F
    flag_lines = [ln for ln in lines if ln.split() and ln.split()[0] == "F"]
    assert flag_lines, "No board line found with F at column 0"
