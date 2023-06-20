from typing import List

from stockshark.piece.piece import Piece
from stockshark.util.chess_exception import ChessException
from stockshark.util.move import Move


class Pawn(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, 100, "P", "p")

    def gen_moves(self, game) -> List[Move]:
        board = game.board
        start_tile = board.pieces_tiles[self]
        moves = []

        try:
            inc = (0, 1) if self.is_white else (0, -1)
            end_tile = start_tile + inc
            if board[end_tile] is None:
                # Corresponding to one step forward
                move = Move(start_tile, end_tile)
                moves.append(move)

                inc = (0, 2) if self.is_white else (0, -2)
                end_tile = start_tile + inc
                if start_tile.row == (1 if self.is_white else 6) and board[end_tile] is None:
                    # Corresponding to two steps forward
                    move = Move(start_tile, end_tile)
                    moves.append(move)
        except ChessException:
            pass

        increments = ((-1, 1), (1, 1)) if self.is_white else ((-1, -1), (1, -1))
        for inc in increments:
            try:
                end_tile = start_tile + inc

                piece = board[end_tile]
                if piece is not None and piece.is_white is not self.is_white:
                    # Corresponding eating a piece in the diagonal
                    move = Move(start_tile, end_tile)
                    moves.append(move)

                elif end_tile == game.en_passant_target:
                    # Corresponding to En Passant
                    move = Move(start_tile, end_tile)
                    moves.append(move)

            except ChessException:
                pass

        return moves
