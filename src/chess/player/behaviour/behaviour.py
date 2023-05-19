from abc import ABC, abstractmethod
from typing import Optional

from chess.chessGame.chessGame import ChessGame
from chess.util.move import Move


class Behaviour(ABC):

    @abstractmethod
    def gen_move(self, game: ChessGame) -> Optional[Move]:
        pass
