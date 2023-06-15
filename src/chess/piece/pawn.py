from typing import List

from chess.piece.piece import Piece
from chess.util.chess_exception import ChessException
from chess.util.move import Move


class Pawn(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, 100, "♟", "♙")

    def gen_moves(self, game) -> List[Move]:
        board = game.board
        start_pos = self.get_pos(board)
        moves = []

        try:
            inc = (0, 1) if self.is_white else (0, -1)
            end_pos = start_pos + inc
            if board[end_pos] is None:
                # Corresponding to one step forward
                move = Move(start_pos, end_pos, self)
                moves.append(move)

                inc = (0, 2) if self.is_white else (0, -2)
                end_pos = start_pos + inc
                if start_pos.row == (1 if self.is_white else 6) and board[end_pos] is None:
                    # Corresponding to two steps forward
                    move = Move(start_pos, end_pos, self)
                    moves.append(move)
        except ChessException:
            pass

        increments = ((-1, 1), (1, 1)) if self.is_white else ((-1, -1), (1, -1))
        for inc in increments:
            try:
                end_pos = start_pos + inc

                piece = board[end_pos]
                if piece is not None and piece.is_white is not self.is_white:
                    # Corresponding eating a piece in the diagonal
                    move = Move(start_pos, end_pos, self, piece)
                    moves.append(move)

                elif end_pos == game.en_passant_target:
                    # Corresponding to En Passant
                    piece_pos = game.en_passant_target + ((0, -1) if self.is_white else (0, 1))
                    piece = board[piece_pos]
                    move = Move(start_pos, end_pos, self, piece)
                    moves.append(move)

            except ChessException:
                pass

        return moves
