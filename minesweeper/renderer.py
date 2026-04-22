from minesweeper.board import Board


class BoardRenderer:
    @staticmethod
    def render(board: Board) -> str:
        rows = []
        for row in range(board.rows):
            symbols = []
            for col in range(board.cols):
                cell = board.cell(row, col)
                if cell.flagged:
                    symbols.append("F")
                elif not cell.revealed:
                    symbols.append(".")
                else:
                    symbols.append(
                        str(cell.adjacent_count) if cell.adjacent_count else " "
                    )
            rows.append(" ".join(symbols))
        return "\n".join(rows) + "\n"
