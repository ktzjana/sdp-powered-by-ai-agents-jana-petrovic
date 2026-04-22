import argparse

from minesweeper.board import Board
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
    print(BoardRenderer.render(board))


if __name__ == "__main__":
    main()
