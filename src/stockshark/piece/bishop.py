from typing import List

from stockshark.piece.piece import Piece
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class Bishop(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, Piece.BISHOP_VALUE, Piece.BISHOP_W, Piece.BISHOP_B)

    def gen_moves(self, game) -> List[Move]:
        return self._gen_slider_moves(game.board, is_diag=True)

    def gen_attacked_tiles(self, game) -> List[Tile]:
        return self._gen_slider_attacked_tiles(game.board, is_diag=True)
