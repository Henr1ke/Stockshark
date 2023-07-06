from typing import Set

from stockshark.piece.piece import Piece
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class Queen(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, Piece.QUEEN_VALUE, Piece.QUEEN_W, Piece.QUEEN_B)

    def gen_moves(self, game) -> Set[Move]:
        board = game.board
        moves = self._gen_slider_moves(board, is_diag=True)
        moves = moves.union(self._gen_slider_moves(board, is_diag=False))
        return moves

    def gen_attacked_tiles(self, game) -> Set[Tile]:
        board = game.board
        attacked_tiles = self._gen_slider_attacked_tiles(board, is_diag=True)
        attacked_tiles = attacked_tiles.union(self._gen_slider_attacked_tiles(board, is_diag=False))
        return attacked_tiles

