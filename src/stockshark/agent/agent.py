from abc import ABC, abstractmethod

from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.util.move import Move


class Agent(ABC):
    @abstractmethod
    def gen_move(self, engine: ChessEngine) -> Move:
        pass
