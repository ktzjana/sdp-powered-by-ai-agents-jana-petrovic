from minesweeper.board import Board, RevealResult


def test_game_be_001_1_s1_reveal_mine_returns_mine_hit():
    # GIVEN - a board where cell (1, 1) is a mine
    board = Board(rows=3, cols=3, mines=0)
    board.cell(1, 1).is_mine = True

    # WHEN
    result = board.reveal(1, 1)

    # THEN
    assert result == RevealResult.MINE_HIT
    assert board.cell(1, 1).revealed is True


def test_game_be_001_1_s2_reveal_safe_cell_returns_ok():
    # GIVEN - a board where cell (2, 2) is a safe numbered cell
    board = Board(rows=3, cols=3, mines=0)

    # WHEN
    result = board.reveal(2, 2)

    # THEN
    assert result == RevealResult.OK
    assert board.cell(2, 2).revealed is True
