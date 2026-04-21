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
