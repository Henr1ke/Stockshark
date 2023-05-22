from abc import ABC, abstractmethod
from typing import Optional

from chess.chessGame.chess_game import ChessGame
from chess.piece.bishop import Bishop
from chess.piece.king import King
from chess.piece.knight import Knight
from chess.piece.pawn import Pawn
from chess.piece.piece import Piece
from chess.piece.queen import Queen
from chess.piece.rook import Rook
from chess.util.move import Move


class Behaviour(ABC):

    @staticmethod
    def get_prio(piece: Piece):
        if isinstance(piece, Pawn):
            return 1
        if isinstance(piece, Knight):
            return 3
        if isinstance(piece, Bishop):
            return 3
        if isinstance(piece, Rook):
            return 5
        if isinstance(piece, Queen):
            return 9
        if isinstance(piece, King):
            return 50

    @abstractmethod
    def gen_move(self, game: ChessGame) -> Optional[Move]:
        pass
