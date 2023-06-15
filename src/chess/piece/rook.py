from typing import List

from chess.piece.piece import Piece
from chess.util.move import Move


class Rook(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, 500, "R", "r")

    def gen_moves(self, game) -> List[Move]:
        return self._gen_slider_moves(game.board, is_diag=False)
