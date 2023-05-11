from typing import List

from chess.piece.piece import Piece
from chess.util.position import Position


class Rook(Piece):

    def gen_positions(self, game) -> List[Position]:
        return self._gen_slider_positions(game.board, is_diag=False)
