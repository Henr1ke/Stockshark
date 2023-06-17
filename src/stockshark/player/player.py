from abc import ABC, abstractmethod
from stockshark.chessGame.chess_game import ChessGame
from stockshark.util.move import Move


class Player(ABC):

    @abstractmethod
    def gen_move(self, game: ChessGame) -> Move:
        pass
