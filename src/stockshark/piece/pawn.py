from typing import Set

from stockshark.piece.piece import Piece
from stockshark.util.chess_exception import ChessException
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class Pawn(Piece):

    def __init__(self, is_white: bool):
        super().__init__(is_white, Piece.PAWN_VALUE, Piece.PAWN_W, Piece.PAWN_B)

    def gen_attacked_tiles(self, game) -> Set[Tile]:
        attacked_tiles = set()
        board = game.board
        start_tile = board.pieces_tiles[self]
        increments = ((-1, 1), (1, 1)) if self.is_white else ((-1, -1), (1, -1))
        for inc in increments:
            try:
                end_tile = start_tile + inc
                attacked_tiles.add(end_tile)
            except ChessException:
                pass
        return attacked_tiles

    def gen_moves(self, game) -> Set[Move]:
        board = game.board
        start_tile = board.pieces_tiles[self]
        moves = set()

        try:
            inc = (0, 1) if self.is_white else (0, -1)
            end_tile = start_tile + inc
            if board[end_tile] is None:
                # Corresponding to one step forward
                moves = moves.union(self.__get_moves(start_tile, end_tile))

                inc = (0, 2) if self.is_white else (0, -2)
                end_tile = start_tile + inc
                if start_tile.row == (1 if self.is_white else 6) and board[end_tile] is None:
                    # Corresponding to two steps forward
                    move = Move(start_tile, end_tile)
                    moves.add(move)
        except ChessException:
            pass

        increments = ((-1, 1), (1, 1)) if self.is_white else ((-1, -1), (1, -1))
        for inc in increments:
            try:
                end_tile = start_tile + inc

                if end_tile == game.ep_target:
                    # Corresponding to En Passant
                    move = Move(start_tile, end_tile)
                    moves.add(move)
                    continue

                piece = board[end_tile]
                if piece is not None and piece.is_white is not self.is_white:
                    # Corresponding eating a piece in the diagonal
                    moves = moves.union(self.__get_moves(start_tile, end_tile))

                # if end_tile == game.ep_target:
                #     # Corresponding to En Passant
                #     move = Move(start_tile, end_tile)
                #     moves.add(move)

            except ChessException:
                pass

        return moves

    def __get_moves(self, start_tile: Tile, end_tile: Tile) -> Set[Move]:
        if self.is_white and start_tile.row == 6 and end_tile.row == 7 or \
                not self.is_white and start_tile.row == 1 and end_tile.row == 0:
            return {
                Move(start_tile, end_tile, Move.PROMOTE_N),
                Move(start_tile, end_tile, Move.PROMOTE_B),
                Move(start_tile, end_tile, Move.PROMOTE_R),
                Move(start_tile, end_tile, Move.PROMOTE_Q),
            }
        return {Move(start_tile, end_tile)}
