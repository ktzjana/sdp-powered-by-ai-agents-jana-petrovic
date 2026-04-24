import argparse

from minesweeper.board import Board
from minesweeper.game import Game
from minesweeper.renderer import BoardRenderer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--rows", type=int, default=5)
    parser.add_argument("--cols", type=int, default=5)
    parser.add_argument("--mines", type=int, default=3)
    args = parser.parse_args()

    if args.seed is not None:
        import random

        random.seed(args.seed)

    board = Board(rows=args.rows, cols=args.cols, mines=args.mines)
    game = Game(board)
    print(BoardRenderer.render(board), end="")

    while True:
        try:
            line = input()
        except EOFError:
            break
        parts = line.strip().split()
        if not parts:
            continue
        if parts[0] == "q":
            break
        if parts[0] == "f" and len(parts) == 3:
            try:
                row, col = int(parts[1]), int(parts[2])
            except ValueError:
                print("Usage: r <row> <col> | f <row> <col> | q")
                continue
            game.flag(row, col)
            print(BoardRenderer.render(board), end="")
        elif parts[0] == "r" and len(parts) == 3:
            try:
                row, col = int(parts[1]), int(parts[2])
            except ValueError:
                print("Usage: r <row> <col> | f <row> <col> | q")
                continue
            game.reveal(row, col)
            print(BoardRenderer.render(board), end="")
            if game.state.name == "WIN":
                print("You win!")
                break
            if game.state.name == "LOSS":
                print("BOOM! You hit a mine.")
                break
        else:
            print("Usage: r <row> <col> | f <row> <col> | q")


if __name__ == "__main__":
    main()
