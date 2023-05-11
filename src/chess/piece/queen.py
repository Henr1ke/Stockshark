from typing import List

from chess.piece.piece import Piece
from chess.util.position import Position


class Queen(Piece):

    def gen_positions(self, game) -> List[Position]:
        board = game.board
        position = self._gen_slider_positions(board, is_diag=True)
        position += self._gen_slider_positions(board, is_diag=False)
        return position
