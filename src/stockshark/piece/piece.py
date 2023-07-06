from abc import ABC, abstractmethod
from typing import List, Tuple, Set

from stockshark.util.chess_exception import ChessException
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class Piece(ABC):
    PAWN_W = "P"
    PAWN_B = "p"
    KNIGHT_W = "N"
    KNIGHT_B = "n"
    BISHOP_W = "B"
    BISHOP_B = "b"
    ROOK_W = "R"
    ROOK_B = "r"
    QUEEN_W = "Q"
    QUEEN_B = "q"
    KING_W = "K"
    KING_B = "k"

    PAWN_VALUE = 100
    KNIGHT_VALUE = 300
    BISHOP_VALUE = 300
    ROOK_VALUE = 500
    QUEEN_VALUE = 900
    KING_VALUE = 10000

    def __init__(self, is_white: bool, value: float, symbol_w: str, symbol_b: str) -> None:
        self.__is_white: bool = is_white
        self.__value: float = value
        self.__symbol: str = symbol_w if is_white else symbol_b

    @property
    def is_white(self) -> bool:
        return self.__is_white

    @property
    def value(self) -> float:
        return self.__value

    @property
    def symbol(self) -> str:
        return self.__symbol

    def __repr__(self) -> str:
        return self.__symbol

    @abstractmethod
    def gen_moves(self, game) -> Set[Move]:
        pass

    @abstractmethod
    def gen_attacked_tiles(self, game) -> Set[Tile]:
        pass

    def _gen_slider_attacked_tiles(self, board, is_diag: bool) -> Set[Tile]:
        start_tile = board.pieces_tiles[self]
        attacked_tiles = set()

        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1)) if is_diag else ((0, 1), (1, 0), (0, -1), (-1, 0))
        for direction in directions:
            try:
                end_tile = start_tile + direction
                while board[end_tile] is None:
                    attacked_tiles.add(end_tile)
                    end_tile += direction
                attacked_tiles.add(end_tile)
            except ChessException:
                pass

        return attacked_tiles

    def _gen_inc_attacked_tiles(self, board, incs: List[Tuple[int, int]]) -> Set[Tile]:
        start_tile = board.pieces_tiles[self]
        attacked_tiles = set()

        for inc in incs:
            try:
                end_tile = start_tile + inc
                attacked_tiles.add(end_tile)
            except ChessException:
                pass

        return attacked_tiles

    def _gen_slider_moves(self, board, is_diag: bool) -> Set[Move]:
        start_tile = board.pieces_tiles[self]
        moves = set()

        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1)) if is_diag else ((0, 1), (1, 0), (0, -1), (-1, 0))
        for direction in directions:
            try:
                end_tile = start_tile + direction
                while board[end_tile] is None:
                    move = Move(start_tile, end_tile)
                    moves.add(move)
                    end_tile += direction

                piece = board[end_tile]
                if piece.is_white is not self.is_white:
                    move = Move(start_tile, end_tile)
                    moves.add(move)
            except ChessException:
                pass

        return moves

    def _gen_inc_moves(self, board, incs: List[Tuple[int, int]]) -> Set[Move]:
        start_tile = board.pieces_tiles[self]
        moves = set()

        for inc in incs:
            try:
                end_tile = start_tile + inc
                piece = board[end_tile]
                if piece is None:
                    move = Move(start_tile, end_tile)
                    moves.add(move)
                elif piece.is_white is not self.is_white:
                    move = Move(start_tile, end_tile)
                    moves.add(move)
            except ChessException:
                pass

        return moves
