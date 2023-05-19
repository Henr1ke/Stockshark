from typing import List

from chess.piece.piece import Piece
from chess.util.chessException import ChessException
from chess.util.position import Position


class Pawn(Piece):

    def gen_positions(self, game) -> List[Position]:
        board = game.board
        start_pos = self.get_pos(board)
        positions = []

        try:
            inc = (0, 1) if self.is_white else (0, -1)
            end_pos = start_pos + inc
            if board[end_pos] is None:
                # Corresponding to one step forward
                positions.append(end_pos)

                inc = (0, 2) if self.is_white else (0, -2)
                end_pos = start_pos + inc
                if start_pos.row == (1 if self.is_white else 6) and board[end_pos] is None:
                    # Corresponding to two steps forward
                    positions.append(end_pos)
        except ChessException:
            pass

        increments = ((-1, 1), (1, 1)) if self.is_white else ((-1, -1), (1, -1))
        for inc in increments:
            try:
                end_pos = start_pos + inc
                piece = board[end_pos]
                if (piece is not None and piece.plays_as_whites is not self.is_white) or end_pos == game.en_passant_target:
                    # Corresponding to En Passant or eating a piece in the diagonal
                    positions.append(end_pos)
            except ChessException:
                pass

        return positions
