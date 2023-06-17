from typing import List

from stockshark.piece.piece import Piece
from stockshark.util.move import Move


class Knight(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, 300, "N", "n")

    def gen_moves(self, game) -> List[Move]:
        increments = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        return self._gen_inc_moves(game.board, increments)
