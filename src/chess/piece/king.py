from typing import List

from chess.piece.piece import Piece
from chess.util.position import Position


class King(Piece):
    def __init__(self, is_white: bool) -> None:
        super().__init__(is_white, False, "♚", "♔")

    def gen_positions(self, board: Board, start_pos: Position) -> List[Position]:
        increments = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        return self._gen_inc_positions(board, start_pos, increments)
