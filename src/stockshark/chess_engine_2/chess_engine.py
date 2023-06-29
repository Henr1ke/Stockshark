from abc import ABC, abstractmethod
from copy import copy
from typing import List


class ChessEngine(ABC):

    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self._new_game(fen)
        self.__fen = self._gen_fen()
        self.__played_moves: List[str] = []
        self.__available_moves: List[str] = self._gen_available_moves()

    @abstractmethod
    def _new_game(self, fen: str) -> None:
        pass

    @abstractmethod
    def _make_move(self, move: str) -> None:
        pass

    @abstractmethod
    def _gen_available_moves(self) -> List[str]:
        pass

    @abstractmethod
    def _gen_fen(self) -> str:
        pass

    def play(self, move: str) -> bool:
        if move not in self.__available_moves:
            return False

        self._make_move(move)

        self.__fen = self._gen_fen()
        self.__played_moves.append(move)
        self.__available_moves: List[str] = self._gen_available_moves()

        return True

    @property
    def fen(self) -> str:
        return self.__fen

    @property
    def played_moves(self) -> List[str]:
        return copy(self.__played_moves)

    @property
    def available_moves(self) -> List[str]:
        return copy(self.__available_moves)
