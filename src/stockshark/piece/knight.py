from typing import Set

from stockshark.piece.piece import Piece
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class Knight(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, Piece.KNIGHT_VALUE, Piece.KNIGHT_W, Piece.KNIGHT_B)

    def gen_moves(self, game) -> Set[Move]:
        increments = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        return self._gen_inc_moves(game.board, increments)

    def gen_attacked_tiles(self, game) -> Set[Tile]:
        increments = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        return self._gen_inc_attacked_tiles(game.board, increments)
