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
        if can_castle_q and board[1, start_tile.row] is None and board[2, start_tile.row] is None \
                and board[3, start_tile.row] is None:
            end_tile = start_tile + (-2, 0)
            move = Move(start_tile, end_tile)
            moves.append(move)

        can_castle_k = ("K" if self.is_white else "k") in game.castlings
        if can_castle_k and board[5, start_tile.row] is None and board[6, start_tile.row] is None:
            end_tile = start_tile + (2, 0)
            move = Move(start_tile, end_tile)
            moves.append(move)

        return moves
