from abc import ABC, abstractmethod
from typing import List, Tuple

from chess.util.chess_exception import ChessException
from chess.util.move import Move
from chess.util.position import Position


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

    def get_pos(self, board) -> Position:
        if self not in board.pieces_pos.keys():
            raise ChessException("The board does not contain the piece")
        return board.pieces_pos[self]

    @abstractmethod
    def gen_moves(self, game) -> List[Move]:
        pass

    def _gen_slider_moves(self, board, is_diag: bool) -> List[Move]:
        start_pos = self.get_pos(board)
        moves = []

        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1)) if is_diag else ((0, 1), (1, 0), (0, -1), (-1, 0))
        for direction in directions:
            try:
                # Adds to possible_pos while the path has no pieces
                end_pos = start_pos + direction
                while board[end_pos] is None:
                    move = Move(start_pos, end_pos, self)
                    moves.append(move)
                    end_pos += direction

                piece = board[end_pos]
                if piece.is_white is not self.is_white:
                    move = Move(start_pos, end_pos, self, piece)
                    moves.append(move)
            except ChessException:
                pass

        return moves

    def _gen_inc_moves(self, board, incs: List[Tuple[int, int]]) -> List[Move]:
        start_pos = self.get_pos(board)
        moves = []

        for inc in incs:
            try:
                end_pos = start_pos + inc
                piece = board[end_pos]
                if piece is None:
                    move = Move(start_pos, end_pos, self)
                    moves.append(move)
                elif piece.is_white is not self.is_white:
                    move = Move(start_pos, end_pos, self, piece)
                    moves.append(move)
            except ChessException:
                pass

        return moves
