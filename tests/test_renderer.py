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
