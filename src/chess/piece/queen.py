from typing import List

from chess.piece.piece import Piece
from chess.util.position import Position


class Queen(Piece):
    def __init__(self, is_white: bool) -> None:
        super().__init__(is_white, "♛", "♕")

    def gen_positions(self, game) -> List[Position]:
        board = game.board
        position = self._gen_slider_positions(board, is_diag=True)
        position += self._gen_slider_positions(board, is_diag=False)
        return position
