from abc import ABC, abstractmethod
from stockshark.chess_engine.game import Game
from stockshark.util.move import Move


class Player(ABC):

    @abstractmethod
    def gen_move(self, game: Game) -> Move:
        pass
