from typing import List

from chess.piece.piece import Piece
from chess.util.position import Position


class King(Piece):
    def __init__(self, is_white: bool) -> None:
        super().__init__(is_white, "♚", "♔")
        # super().__init__(is_white, "K", "k")

    def gen_positions(self, game) -> List[Position]:
        board = game.board

        start_pos = self.get_pos(board)

        increments = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        positions = self._gen_inc_positions(board, increments)

        # Adds castling positions to the possible positions if possible
        can_castle_q = ("Q" if self.is_white else "q") in game.castlings
        can_castle_k = ("K" if self.is_white else "k") in game.castlings
        if can_castle_q and board[1, start_pos.row] is None and board[2, start_pos.row] is None \
                and board[3, start_pos.row] is None:
            positions.append(start_pos + (-2, 0))
        if can_castle_k and board[5, start_pos.row] is None and board[6, start_pos.row] is None:
            positions.append(start_pos + (2, 0))

        return positions
