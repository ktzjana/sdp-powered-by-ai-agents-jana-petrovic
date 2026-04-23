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


def test_game_be_001_3_s2_check_win_returns_false_when_safe_cells_remain():
    # GIVEN - a game where multiple safe cells are still unrevealed
    # 2x2 board, 1 mine at (0,0); safe cells: (0,1),(1,0),(1,1)
    board = Board(rows=2, cols=2, mines=0)
    board.cell(0, 0).is_mine = True
    board.compute_adjacent_counts()
    game = Game(board)

    # WHEN - only one safe cell is revealed
    game.reveal(0, 1)

    # THEN
    assert game.check_win() is False
    assert game.state == GameState.PLAYING


def test_game_story_001_s1_reveal_numbered_cell():
    # GIVEN - a board with a safe cell (0,0) that has adjacent_count > 0
    from minesweeper.renderer import BoardRenderer

    board = Board(rows=2, cols=2, mines=0)
    board.cell(0, 1).is_mine = True
    board.compute_adjacent_counts()
    game = Game(board)

    # WHEN - the player reveals cell (0,0)
    game.reveal(0, 0)

    # THEN - cell is marked revealed; board renders adjacent count; game continues
    assert board.cell(0, 0).revealed is True
    assert board.cell(0, 0).adjacent_count == 1
    output = BoardRenderer.render(board)
    assert "1" in output
    assert game.state.name == "PLAYING"


def test_game_story_001_s2_reveal_mine_ends_game_as_loss():
    # GIVEN - the game started with --seed 42 (mines at (0,0), (0,3), (4,0))
    import os
    import subprocess
    import sys
    from pathlib import Path

    env = {**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)}

    # WHEN - the player reveals the mine cell at (0,0)
    result = subprocess.run(
        [
            sys.executable,
            "minesweeper/cli.py",
            "--seed",
            "42",
            "--rows",
            "5",
            "--cols",
            "5",
            "--mines",
            "3",
        ],
        input="r 0 0\n",
        capture_output=True,
        text=True,
        env=env,
    )

    # THEN - loss message is printed; game loop exits
    assert "BOOM! You hit a mine." in result.stdout


def test_game_story_001_s3_reveal_empty_cell_triggers_flood_fill():
    # GIVEN - a board where (0,0) is empty (adjacent_count==0, no mine)
    # Layout: mine only at (2,2); (0,0),(0,1),(1,0),(1,1) are empty
    board = Board(rows=3, cols=3, mines=0)
    board.cell(2, 2).is_mine = True
    board.compute_adjacent_counts()
    game = Game(board)

    # WHEN - the player reveals (0,0)
    game.reveal(0, 0)

    # THEN - (0,0) and connected empty cells are revealed
    assert board.cell(0, 0).revealed is True
    assert board.cell(0, 1).revealed is True
    assert board.cell(1, 0).revealed is True
    assert board.cell(1, 1).revealed is True
    # THEN - numbered border cells adjacent to empty region are also revealed
    assert board.cell(0, 2).revealed is True
    assert board.cell(2, 0).revealed is True
    # THEN - mine cell is not revealed
    assert board.cell(2, 2).revealed is False
