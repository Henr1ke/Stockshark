from typing import List

from chess.piece.piece import Piece
from chess.util.position import Position


class Rook(Piece):
    def __init__(self, is_white: bool) -> None:
        super().__init__(is_white, True, "♜", "♖")

    def gen_positions(self, board: Board, start_pos: Position) -> List[Position]:
        return self._gen_slider_positions(board, start_pos, is_diag=False)