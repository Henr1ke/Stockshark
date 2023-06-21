from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Optional, List

from stockshark.chess_engine.board import Board
from stockshark.chess_engine.state import State
from stockshark.piece.piece import Piece
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class GameEngine(ABC):

    @property
    @abstractmethod
    def board(self) -> Board:
        pass

    @property
    @abstractmethod
    def is_white_turn(self) -> bool:
        pass

    @property
    @abstractmethod
    def castlings(self) -> str:
        pass

    @property
    @abstractmethod
    def en_passant_target(self) -> Optional[Tile]:
        pass

    @property
    @abstractmethod
    def halfclock(self) -> int:
        pass

    @property
    @abstractmethod
    def fullclock(self) -> int:
        pass

    @property
    @abstractmethod
    def played_moves(self) -> List[Move]:
        pass

    @property
    @abstractmethod
    def state(self) -> State:
        pass

    @abstractmethod
    def __copy__(self) -> GameEngine:
        pass

    @abstractmethod
    def get_available_pieces_tiles(self) -> Dict[Piece, Tile]:
        pass

    @abstractmethod
    def get_legal_piece_moves(self, piece: Piece) -> List[Move]:
        pass

    @abstractmethod
    def gen_fen_str(self) -> str:
        pass

    @abstractmethod
    def evaluate_game(self) -> float:
        pass

    @abstractmethod
    def evaluate_move(self, move: Move) -> float:
        pass

    @abstractmethod
    def make_move(self, move: Move, is_test=False) -> bool:
        pass
