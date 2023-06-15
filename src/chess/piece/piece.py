from abc import ABC, abstractmethod
from typing import List, Tuple

from chess.util.chess_exception import ChessException
from chess.util.position import Position


class Piece(ABC):

    def __init__(self, is_white: bool, value: float) -> None:
        self.__is_white: bool = is_white
        self.__value: float = value

    @property
    def is_white(self) -> bool:
        return self.__is_white

    @property
    def value(self) -> float:
        return self.__value

    @abstractmethod
    def gen_positions(self, game) -> List[Position]:
        pass

    def get_pos(self, board) -> Position:
        if self not in board.pieces_pos.keys():
            raise ChessException("The board does not contain the piece to generate the positions")
        return board.pieces_pos[self]

    def _gen_slider_positions(self, board, is_diag: bool) -> List[Position]:
        start_pos = board.pieces_pos[self]
        positions = []

        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1)) if is_diag else ((0, 1), (1, 0), (0, -1), (-1, 0))
        for direction in directions:
            try:
                # Adds to possible_pos while the path has no pieces
                end_pos = start_pos + direction
                while board[end_pos] is None:
                    positions.append(end_pos)
                    end_pos += direction

                if board[end_pos].is_white is not self.is_white:
                    positions.append(end_pos)
            except ChessException:
                pass

        return positions

    def _gen_inc_positions(self, board, incs: List[Tuple[int, int]]) -> List[Position]:
        start_pos = board.pieces_pos[self]
        positions = []

        for inc in incs:
            try:
                end_pos = start_pos + inc
                piece = board[end_pos]
                if piece is None or piece.is_white is not self.is_white:
                    positions.append(end_pos)
            except ChessException:
                pass

        return positions
