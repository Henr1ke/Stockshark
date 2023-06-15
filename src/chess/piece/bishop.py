from typing import List

from chess.piece.piece import Piece
from chess.util.position import Position


class Bishop(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, 300)

    def gen_positions(self, game) -> List[Position]:
        return self._gen_slider_positions(game.board, is_diag=True)
