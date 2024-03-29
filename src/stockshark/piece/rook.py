from typing import Set

from stockshark.piece.piece import Piece
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class Rook(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, Piece.ROOK_VALUE, Piece.ROOK_W, Piece.ROOK_B)

    def gen_moves(self, engine) -> Set[Move]:
        return self._gen_slider_moves(engine.board, is_diag=False)

    def gen_attacked_tiles(self, engine) -> Set[Tile]:
        return self._gen_slider_attacked_tiles(engine.board, is_diag=False)
