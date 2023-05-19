from abc import ABC, abstractmethod
from typing import Dict

from chess.piece.piece import Piece
from chess.chessGame.chessGame import ChessGame
from chess.util.move import Move
from chess.util.position import Position


class Player(ABC):

    @abstractmethod
    def gen_move(self, game: ChessGame) -> Move:
        pass
