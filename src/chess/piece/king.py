from typing import List

from chess.piece.piece import Piece
from chess.util.move import Move


class King(Piece):
    def __init__(self, is_white: bool):
        super().__init__(is_white, 3000, "♚︎", "♔")

    def gen_moves(self, game) -> List[Move]:
        board = game.board
        start_pos = self.get_pos(board)

        increments = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        moves = self._gen_inc_moves(board, increments)

        can_castle_q = ("Q" if self.is_white else "q") in game.castlings
        if can_castle_q and board[1, start_pos.row] is None and board[2, start_pos.row] is None \
                and board[3, start_pos.row] is None:
            end_pos = start_pos + (-2, 0)
            move = Move(start_pos, end_pos, self)
            moves.append(move)

        can_castle_k = ("K" if self.is_white else "k") in game.castlings
        if can_castle_k and board[5, start_pos.row] is None and board[6, start_pos.row] is None:
            end_pos = start_pos + (2, 0)
            move = Move(start_pos, end_pos, self)
            moves.append(move)

        return moves
