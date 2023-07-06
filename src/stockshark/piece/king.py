from typing import Set

from stockshark.piece.piece import Piece
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class King(Piece):
    def __init__(self, is_white: bool):
        super().__init__(is_white, Piece.KING_VALUE, Piece.KING_W, Piece.KING_B)

    def gen_moves(self, game) -> Set[Move]:
        board = game.board
        start_tile = board.pieces_tiles[self]

        increments = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        moves = self._gen_inc_moves(board, increments)

        board = game.board

        can_castle_q = ("Q" if self.is_white else "q") in game.castling_rights

        if can_castle_q and start_tile.name not in game.attacked_tiles and \
                not self._path_blocked(board, start_tile.row, 1, 4) and \
                not self._path_attacked(game, start_tile.row, 2, 4):
            end_tile = start_tile + (-2, 0)
            move = Move(start_tile, end_tile)
            moves.add(move)

        can_castle_k = ("K" if self.is_white else "k") in game.castling_rights

        if can_castle_k and start_tile.name not in game.attacked_tiles and \
                not self._path_blocked(board, start_tile.row, 6, 4) and \
                not self._path_attacked(game, start_tile.row, 6, 4):
            end_tile = start_tile + (2, 0)
            move = Move(start_tile, end_tile)
            moves.add(move)

        return moves

    def gen_attacked_tiles(self, game) -> Set[Tile]:
        increments = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        return self._gen_inc_attacked_tiles(game.board, increments)

    @staticmethod
    def _path_blocked(board, row: int, start_col: int, end_col: int) -> bool:
        for i in range(start_col, end_col, 1 if start_col < end_col else -1):
            if board[i, row] is not None:
                return True
        return False

    @staticmethod
    def _path_attacked(game, row: int, start_col: int, end_col: int) -> bool:
        for i in range(start_col, end_col, 1 if start_col < end_col else -1):
            if Tile(i, row).name in game.attacked_tiles:
                return True
        return False
