from abc import ABC, abstractmethod

from stockshark.chess_engine.chess_engine import ChessEngine


class Agent(ABC):
    @abstractmethod
    def gen_move(self, engine: ChessEngine) -> str:
        pass
