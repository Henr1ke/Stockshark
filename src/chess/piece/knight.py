from typing import List

from chess.piece.piece import Piece
from chess.util.position import Position


class Knight(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, 300)


    def gen_positions(self, game) -> List[Position]:
        increments = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        return self._gen_inc_positions(game.board, increments)
