from typing import List

from stockshark.piece.piece import Piece
from stockshark.util.move import Move


class Queen(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, 900, "Q", "q")

    def gen_moves(self, game) -> List[Move]:
        board = game.board
        moves = self._gen_slider_moves(board, is_diag=True)
        moves += self._gen_slider_moves(board, is_diag=False)
        return moves
