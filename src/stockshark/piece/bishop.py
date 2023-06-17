from typing import List

from stockshark.piece.piece import Piece
from stockshark.util.move import Move


class Bishop(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, 300, "B", "b")

    def gen_moves(self, game) -> List[Move]:
        return self._gen_slider_moves(game.board, is_diag=True)
