from minesweeper.board import Board
from minesweeper.renderer import BoardRenderer


def test_board_fe_001_1_s1_initial_board_renders_all_cells_as_hidden():
    # GIVEN - a 3x2 board with no cells revealed or flagged
    board = Board(rows=3, cols=2, mines=0)

    # WHEN
    output = BoardRenderer.render(board)

    # THEN - every cell shows the hidden symbol; grid matches configured dimensions
    rows = output.strip().splitlines()
    assert len(rows) == 3
    for row in rows:
        symbols = row.split()
        assert len(symbols) == 2
        assert all(s == "." for s in symbols)


def test_game_fe_003_1_s1_flagged_cell_renders_with_flag_marker():
    # GIVEN - cell (1, 4) is flagged
    board = Board(rows=3, cols=5, mines=0)
    board.cell(1, 4).flagged = True

    # WHEN
    output = BoardRenderer.render(board)

    # THEN - position (1, 4) displays "F"; all other cells show hidden symbol
    rows = output.strip().splitlines()
    assert rows[1].split()[4] == "F"
    assert all(s == "." for s in rows[0].split())
    assert rows[1].split()[:4] == [".", ".", ".", "."]
    assert all(s == "." for s in rows[2].split())


def test_game_fe_003_1_s2_unflagged_cell_reverts_to_hidden_marker():
    # GIVEN - cell (1, 4) was flagged and has just been unflagged
    board = Board(rows=3, cols=5, mines=0)
    board.cell(1, 4).flagged = True
    board.toggle_flag(1, 4)

    # WHEN
    output = BoardRenderer.render(board)

    # THEN - position (1, 4) displays the hidden symbol again
    rows = output.strip().splitlines()
    assert rows[1].split()[4] == "."


def test_cli_be_002_1_s1_renderer_outputs_correct_rows_and_columns():
    # GIVEN - a 3x4 board with all cells hidden
    board = Board(rows=3, cols=4, mines=0)

    # WHEN
    output = BoardRenderer.render(board)

    # THEN - exactly 3 rows, each with exactly 4 cell symbols
    rows = output.strip().splitlines()
    assert len(rows) == 3
    for row in rows:
        assert len(row.split()) == 4


def test_cli_be_002_1_s2_renderer_uses_distinct_symbols():
    # GIVEN - (0,0) hidden, (0,1) flagged, (0,2) revealed with adjacent_count==1
    board = Board(rows=1, cols=3, mines=0)
    board.cell(0, 1).flagged = True
    board.cell(0, 2).revealed = True
    board.cell(0, 2).adjacent_count = 1

    # WHEN
    output = BoardRenderer.render(board)

    # THEN
    symbols = output.strip().split()
    assert symbols[0] == "."
    assert symbols[1] == "F"
    assert symbols[2] == "1"


def test_cli_fe_002_1_s1_board_printed_after_reveal_action():
    # GIVEN - the CLI is running with no mines
    import os
    import subprocess
    import sys
    from pathlib import Path

    env = {**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)}

    # WHEN - the player enters "r 0 0" then "q"
    result = subprocess.run(
        [
            sys.executable,
            "minesweeper/cli.py",
            "--rows",
            "3",
            "--cols",
            "3",
            "--mines",
            "0",
        ],
        input="r 0 0\nq\n",
        capture_output=True,
        text=True,
        env=env,
    )

    # THEN - initial board + updated board both printed before exit
    assert result.returncode == 0, result.stderr
    # Two renders: initial (3 rows) + after reveal (3 rows) = at least 6 lines
    assert len(result.stdout.splitlines()) >= 6
