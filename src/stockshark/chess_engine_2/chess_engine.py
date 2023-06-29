from abc import ABC, abstractmethod
from copy import copy
from typing import List


class ChessEngine(ABC):

    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self._new_game(fen)
        self.__played_moves: List[str] = []
        self.__update_fen_fields()
        self.__available_moves: List[str] = self._gen_available_moves()

    def __update_fen_fields(self):
        self.__fen = self._gen_fen()

        fen_fields = self.__fen.split(" ")
        self.__piece_arrangement: str = fen_fields[0]
        self.__turn: str = fen_fields[1]
        self.__castling_rights: str = fen_fields[2]
        self.__ep_target: str = fen_fields[3]
        self.__halfclock: int = int(fen_fields[4])
        self.__fullclock: int = int(fen_fields[5])

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

        self.__played_moves.append(move)
        self.__update_fen_fields()
        self.__available_moves: List[str] = self._gen_available_moves()

        return True

    @property
    def fen(self) -> str:
        return self.__fen

    @property
    def piece_arrangement(self) -> str:
        return self.__piece_arrangement

    @property
    def turn(self) -> str:
        return self.__turn

    @property
    def castling_rights(self) -> str:
        return self.__castling_rights

    @property
    def ep_target(self) -> str:
        return self.__ep_target

    @property
    def halfclock(self) -> int:
        return self.__halfclock

    @property
    def fullclock(self) -> int:
        return self.__fullclock

    @property
    def played_moves(self) -> List[str]:
        return copy(self.__played_moves)

    @property
    def available_moves(self) -> List[str]:
        return copy(self.__available_moves)
