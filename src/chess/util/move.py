from __future__ import annotations

from chess.util.chess_exception import ChessException
from chess.util.position import Position


class Move:
    def __init__(self, start_pos: Position, end_pos: Position, piece, eaten_piece=None) -> None:
        if start_pos == end_pos:
            raise ChessException("A move cannot start and end on itself")
        if eaten_piece is not None and piece.is_white == eaten_piece.is_white:
            raise ChessException("A piece cannot eat another piece of the same color")

        self.__start_pos: Position = start_pos
        self.__end_pos: Position = end_pos
        self.__piece = piece
        self.__eaten_piece = eaten_piece

    def __eq__(self, other: Move) -> bool:
        return isinstance(other, Move) and self.start_pos == other.start_pos and self.end_pos == other.end_pos \
            and self.__eaten_piece == other.eaten_piece

    def __gt__(self, other: Move) -> bool:
        return self.value() > other.value()

    def __lt__(self, other: Move) -> bool:
        return self.value() < other.value()

    def __repr__(self) -> str:
        eaten_piece_symbol = "" if self.__eaten_piece is None else self.__eaten_piece.symbol
        return f"[{self.__piece.symbol} {self.__start_pos} -> {self.__end_pos} {eaten_piece_symbol}]"

    def value(self) -> float:
        value = 0 if self.__eaten_piece is None else self.__eaten_piece.value
        return value

    @property
    def start_pos(self) -> Position:
        return self.__start_pos

    @property
    def end_pos(self) -> Position:
        return self.__end_pos

    @property
    def piece(self):
        return self.__piece

    @property
    def eaten_piece(self):
        return self.__eaten_piece
