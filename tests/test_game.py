from minesweeper.board import Board, RevealResult
from minesweeper.game import Game, GameState


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


def test_game_be_001_2_s1_flood_fill_reveals_connected_empty_cells():
    # GIVEN - a 3x3 board: (0,0),(0,1),(1,0),(1,1) are empty;
    # mines at (2,2) only; border cells (0,2),(1,2),(2,0),(2,1) are numbered
    board = Board(rows=3, cols=3, mines=0)
    board.cell(2, 2).is_mine = True
    board.compute_adjacent_counts()
    # (0,0),(0,1),(1,0),(1,1) should have adjacent_count==0 (no adjacent mine)
    # (0,2),(1,2),(2,0),(2,1) should have adjacent_count>0

    # WHEN
    result = board.reveal(0, 0)

    # THEN
    assert result == RevealResult.OK
    # all connected empty cells are revealed
    assert board.cell(0, 0).revealed is True
    assert board.cell(0, 1).revealed is True
    assert board.cell(1, 0).revealed is True
    assert board.cell(1, 1).revealed is True
    # numbered border cells adjacent to the empty region are also revealed
    assert board.cell(0, 2).revealed is True
    assert board.cell(1, 2).revealed is True
    assert board.cell(2, 0).revealed is True
    assert board.cell(2, 1).revealed is True
    # mine cell is NOT revealed
    assert board.cell(2, 2).revealed is False


def test_game_be_001_2_s2_flood_fill_does_not_revisit_revealed_cells():
    # GIVEN - cell (0, 0) has already been revealed
    board = Board(rows=3, cols=3, mines=0)
    board.cell(0, 0).revealed = True

    # WHEN - board.reveal(0, 0) is called again
    result = board.reveal(0, 0)

    # THEN - board state is unchanged and no error occurs
    assert result == RevealResult.OK
    assert board.cell(0, 0).revealed is True
    # all other cells remain unrevealed
    assert board.cell(0, 1).revealed is False
    assert board.cell(1, 0).revealed is False


def test_game_be_001_3_s1_check_win_returns_true_after_last_safe_reveal():
    # GIVEN - a game with one safe cell remaining unrevealed
    # 2x2 board, 1 mine at (0,0); safe cells: (0,1),(1,0),(1,1)
    board = Board(rows=2, cols=2, mines=0)
    board.cell(0, 0).is_mine = True
    board.compute_adjacent_counts()
    game = Game(board)
    # reveal all safe cells except (1, 1)
    game.reveal(0, 1)
    game.reveal(1, 0)

    # WHEN - the last safe cell is revealed
    game.reveal(1, 1)

    # THEN
    assert game.check_win() is True
    assert game.state == GameState.WIN
