from abc import ABC, abstractmethod
from typing import List, Tuple

from stockshark.util.chess_exception import ChessException
from stockshark.util.move import Move


class Piece(ABC):

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
    def gen_moves(self, game) -> List[Move]:
        pass

    def _gen_slider_moves(self, board, is_diag: bool) -> List[Move]:
        start_tile = board.pieces_tiles[self]
        moves = []

        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1)) if is_diag else ((0, 1), (1, 0), (0, -1), (-1, 0))
        for direction in directions:
            try:
                end_tile = start_tile + direction
                while board[end_tile] is None:
                    move = Move(start_tile, end_tile)
                    moves.append(move)
                    end_tile += direction

                piece = board[end_tile]
                if piece.is_white is not self.is_white:
                    move = Move(start_tile, end_tile)
                    moves.append(move)
            except ChessException:
                pass

        return moves

    def _gen_inc_moves(self, board, incs: List[Tuple[int, int]]) -> List[Move]:
        start_tile = board.pieces_tiles[self]
        moves = []

        for inc in incs:
            try:
                end_tile = start_tile + inc
                piece = board[end_tile]
                if piece is None:
                    move = Move(start_tile, end_tile)
                    moves.append(move)
                elif piece.is_white is not self.is_white:
                    move = Move(start_tile, end_tile)
                    moves.append(move)
            except ChessException:
                pass

        return moves
