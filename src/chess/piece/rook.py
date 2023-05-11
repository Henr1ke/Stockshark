from typing import List

from chess.piece.piece import Piece
from chess.util.position import Position


class Rook(Piece):
    def __init__(self, is_white: bool) -> None:
        super().__init__(is_white, "♜", "♖")
        # super().__init__(is_white, "R", "r")

    def gen_positions(self, game) -> List[Position]:
        return self._gen_slider_positions(game.board, is_diag=False)
