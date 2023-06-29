from typing import List

from stockshark.piece.piece import Piece
from stockshark.util.move import Move


class King(Piece):
    def __init__(self, is_white: bool):
        super().__init__(is_white, 3000, "K", "k")

    def gen_moves(self, game) -> List[Move]:
        board = game.board
        start_tile = board.pieces_tiles[self]

        increments = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        moves = self._gen_inc_moves(board, increments)

        can_castle_q = ("Q" if self.is_white else "q") in game.castlings
        # if can_castle_q and board[1, start_tile.row] is None and board[2, start_tile.row] is None \
        #         and board[3, start_tile.row] is None:
        if can_castle_q and self._path_unblocked(board, start_tile.row, 1, 4):
            end_tile = start_tile + (-2, 0)
            move = Move(start_tile, end_tile)
            moves.append(move)

        can_castle_k = ("K" if self.is_white else "k") in game.castlings
        # if can_castle_k and board[5, start_tile.row] is None and board[6, start_tile.row] is None:
        if can_castle_k and self._path_unblocked(board, start_tile.row, 6, 4):
            end_tile = start_tile + (2, 0)
            move = Move(start_tile, end_tile)
            moves.append(move)

        return moves

    def _path_unblocked(self, board, row: int, start_col: int, end_col: int) -> bool:
        for i in range(start_col, end_col, 1 if start_col < end_col else -1):
            if board[i, row] is not None:
                return False
        return True
        # return board[1, row] is None and board[2, row] is None and board[3, row] is None

    # def _path_not_attacked(self, game, row: int, start_col: int, end_col: int) -> bool:
    #     for i in range(start_col, end_col, 1 if start_col < end_col else -1):
    #         if game.is_tile_attacked(Tile(i, row), not self.is_white):
    #             return False
    #     return True
    #     # return board[1, row] is None and board[2, row] is None and board[3, row] is None
