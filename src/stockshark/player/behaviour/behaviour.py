from abc import ABC, abstractmethod
from typing import Optional

from stockshark.chess_engine.game import Game
from stockshark.piece.bishop import Bishop
from stockshark.piece.king import King
from stockshark.piece.knight import Knight
from stockshark.piece.pawn import Pawn
from stockshark.piece.piece import Piece
from stockshark.piece.queen import Queen
from stockshark.piece.rook import Rook
from stockshark.util.move import Move


class Behaviour(ABC):

    @abstractmethod
    def gen_move(self, game: Game) -> Optional[Move]:
        pass
