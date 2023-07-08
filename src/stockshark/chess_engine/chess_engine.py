from __future__ import annotations

from abc import ABC, abstractmethod
from copy import copy
from typing import List, Optional, Set


class ChessEngine(ABC):

    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self._new_game(fen)
        self.__fen = fen
        self.__played_moves: List[str] = []
        self.__available_moves = sorted(self._gen_available_moves())

    def __copy__(self) -> ChessEngine:
        cls = self.__class__
        engine = cls.__new__(cls)
        for key, value in self.__dict__.items():
            setattr(engine, key, copy(value))
        return engine

    @abstractmethod
    def _new_game(self, fen: str) -> None:
        pass

    @abstractmethod
    def _make_move(self, move: str) -> None:
        pass

    @abstractmethod
    def _gen_available_moves(self) -> Set[str]:
        pass

    @abstractmethod
    def _gen_fen(self) -> str:
        pass

    @abstractmethod
    def get_piece_at(self, tile: str) -> Optional[str]:
        pass

    @abstractmethod
    def is_in_check(self, is_white_side: bool) -> bool:
        pass

    def play(self, move: str) -> bool:
        if move not in self.__available_moves:
            return False

        self._make_move(move)

        self.__fen = self._gen_fen()
        self.__played_moves.append(move)
        self.__available_moves = sorted(self._gen_available_moves())

        return True

    def game_finished(self) -> bool:
        return len(self.available_moves) == 0

    @property
    def fen(self) -> str:
        return self.__fen

    @property
    def played_moves(self) -> List[str]:
        return copy(self.__played_moves)

    @property
    def available_moves(self) -> List[str]:
        halfmove = int(self.__fen.split(" ")[-2])
        if halfmove > 100:
            return []
        # return copy(self.__available_moves)
        # Only alows promotion to queen
        return [move for move in self.__available_moves if move[-1].isdigit() or move[-1] == "q"]
