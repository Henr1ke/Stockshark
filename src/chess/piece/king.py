from typing import List

from chess.piece.piece import Piece
from chess.util.chessException import ChessException
from chess.util.position import Position


class King(Piece):
    def __init__(self, is_white: bool) -> None:
        super().__init__(is_white, "♚", "♔")

    def gen_positions(self, game) -> List[Position]:
        board = game.board

        start_pos = self.get_position(board)

        increments = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        positions = self._gen_inc_positions(board, start_pos, increments)

        # Adds castling positions to the possible positions if possible
        castling_rights = game.get_castlings(self.is_white)
        if castling_rights[0] and board[1, start_pos.row] is None and board[2, start_pos.row] is None \
                and board[3, start_pos.row] is None:
            positions.append(start_pos + (-2, 0))
        if castling_rights[1] and board[5, start_pos.row] is None and board[6, start_pos.row] is None:
            positions.append(start_pos + (2, 0))

        return positions
