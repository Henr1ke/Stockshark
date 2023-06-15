from __future__ import annotations

from typing import Optional

from chess.piece.piece import Piece
from chess.util.chess_exception import ChessException
from chess.util.position import Position


class Move:
    def __init__(self, start_pos: Position, end_pos: Position, eaten_piece: Optional[Piece] = None) -> None:
        if start_pos == end_pos:
            raise ChessException("A move cannot start and end on itself")

        self.__start_pos: Position = start_pos
        self.__end_pos: Position = end_pos
        self.__eaten_piece: Optional[Piece] = eaten_piece

    def __eq__(self, other: Move) -> bool:
        return isinstance(other,
                          Move) and self.start_pos == other.start_pos and self.end_pos == other.end_pos and self.__eaten_piece == other.eaten_piece

    def __gt__(self, other: Move) -> bool:
        if self.__eaten_piece is not None:
            if other.__eaten_piece is None:
                return True
            return self.__eaten_piece.value > other.__eaten_piece.value
        return False

    def __lt__(self, other: Move) -> bool:
        if self.__eaten_piece is not None:
            if other.__eaten_piece is None:
                return False
            return self.__eaten_piece.value < other.__eaten_piece.value
        return False

    def __repr__(self) -> str:
        return f"[{self.start_pos} -> {self.end_pos}]"

    @property
    def start_pos(self) -> Position:
        return self.__start_pos

    @property
    def end_pos(self) -> Position:
        return self.__end_pos

    @property
    def eaten_piece(self) -> Optional[Piece]:
        return self.__eaten_piece
