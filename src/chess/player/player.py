from abc import ABC, abstractmethod
from chess.chessGame.chess_game import ChessGame
from chess.util.move import Move


class Player(ABC):

    @abstractmethod
    def gen_move(self, game: ChessGame) -> Move:
        pass
