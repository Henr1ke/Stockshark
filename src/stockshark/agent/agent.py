from abc import ABC, abstractmethod
from stockshark.chess_engine.game_engine import GameEngine
from stockshark.util.move import Move


class Agent(ABC):

    @abstractmethod
    def gen_move(self, game: GameEngine) -> Move:
        pass
