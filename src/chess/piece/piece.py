from abc import ABC, abstractmethod
from typing import List, Tuple

from chess.util.chessException import ChessException
from chess.util.position import Position


class Piece(ABC):
    def __init__(self, is_white: bool, is_slider: bool, w_symbol: str, b_symbol: str) -> None:
        self.__is_white: bool = is_white
        self.__is_slider: bool = is_slider
        self.__symbol: str = w_symbol if is_white else b_symbol

    def __repr__(self) -> str:
        return self.__symbol

    @property
    def is_white(self) -> bool:
        return self.__is_white

    @property
    def is_slider(self) -> bool:
        return self.__is_slider

    @abstractmethod
    def gen_positions(self, board, start_pos: Position) -> List[Position]:
        pass

    def _gen_slider_positions(self, board, start_pos: Position, is_diag: bool) -> List[Position]:
        possible_pos = []

        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1)) if is_diag else ((0, 1), (1, 0), (0, -1), (-1, 0))
        for direction in directions:
            try:
                # Adds to possible_pos while the path has no pieces
                end_pos = start_pos + direction
                while board[end_pos] is None:
                    possible_pos.append(end_pos)
                    end_pos += direction

                if board[end_pos].is_white is not self.is_white:
                    possible_pos.append(end_pos)
            except ChessException:
                pass

        return possible_pos

    def _gen_inc_positions(self, board, start_pos: Position, incs: List[Tuple[int, int]]) -> List[Position]:
        possible_pos = []

        for inc in incs:
            try:
                end_pos = start_pos + inc
                piece = board[end_pos]
                if piece is None or piece.is_white is not self.is_white:
                    possible_pos.append(end_pos)
            except ChessException:
                pass

        return possible_pos
