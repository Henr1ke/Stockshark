from __future__ import annotations

from abc import ABC, abstractmethod
from copy import copy
from typing import List, Optional, Set

from stockshark.piece.piece import Piece
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class ChessEngine(ABC):

    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.__fen = fen
        self.__played_moves: List[Move] = []
        self.__atacked_tiles: List[Tile] = []
        self.__available_moves: List[Move] = []

        self._new_game(fen)
        self.__atacked_tiles: List[Tile] = sorted(self._gen_attacked_tiles())
        self.__available_moves: List[Move] = sorted(self._gen_available_moves())

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
    def _make_move(self, move: Move) -> None:
        pass

    @abstractmethod
    def _gen_attacked_tiles(self) -> Set[Tile]:
        pass

    @abstractmethod
    def _gen_available_moves(self) -> Set[Move]:
        pass

    @abstractmethod
    def _gen_fen(self) -> str:
        pass

    @abstractmethod
    def get_piece_at(self, tile: Tile) -> Optional[str]:
        pass

    @abstractmethod
    def is_in_check(self, is_white_side: bool) -> bool:
        pass

    def play(self, move: Move) -> bool:
        if move not in self.__available_moves:
            return False # TODO nao está a verificar bema igualdade entre moves

        self._make_move(move)

        self.__fen = self._gen_fen()
        self.__played_moves.append(move)
        self.__atacked_tiles = sorted(self._gen_attacked_tiles())
        self.__available_moves = sorted(self._gen_available_moves())

        return True

    def game_finished(self) -> bool:
        return len(self.available_moves) == 0

    @property
    def fen(self) -> str:
        return self.__fen

    @property
    def played_moves(self) -> List[Move]:
        return copy(self.__played_moves)

    @property
    def available_moves(self) -> List[Move]:
        halfmove = int(self.__fen.split(" ")[-2])
        if halfmove >= 100:
            return []
        return copy(self.__available_moves)

    @property
    def attacked_tiles(self) -> List[Tile]:
        return copy(self.__atacked_tiles)
