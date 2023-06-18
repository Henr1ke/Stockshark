from __future__ import annotations

from stockshark.util.chess_exception import ChessException
from stockshark.util.position import Position


class Move:
    def __init__(self, start_pos: Position, end_pos: Position) -> None:
        if start_pos == end_pos:
            raise ChessException("A move cannot start and end on itself")

        self.__start_pos: Position = start_pos
        self.__end_pos: Position = end_pos

    def __eq__(self, other: Move) -> bool:
        return isinstance(other, Move) and self.start_pos == other.start_pos and self.end_pos == other.end_pos

    def __repr__(self) -> str:
        return f"{self.__start_pos}{self.__end_pos}"

    @property
    def start_pos(self) -> Position:
        return self.__start_pos

    @property
    def end_pos(self) -> Position:
        return self.__end_pos
