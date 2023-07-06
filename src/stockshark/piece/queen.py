from typing import List

from stockshark.piece.piece import Piece
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class Queen(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, Piece.QUEEN_VALUE, Piece.QUEEN_W, Piece.QUEEN_B)

    def gen_moves(self, game) -> List[Move]:
        board = game.board
        moves = self._gen_slider_moves(board, is_diag=True)
        moves += self._gen_slider_moves(board, is_diag=False)
        return moves

    def gen_attacked_tiles(self, game) -> List[Tile]:
        board = game.board
        attacked_tiles = self._gen_slider_attacked_tiles(board, is_diag=True)
        attacked_tiles += self._gen_slider_attacked_tiles(board, is_diag=False)
        return attacked_tiles

