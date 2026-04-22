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
