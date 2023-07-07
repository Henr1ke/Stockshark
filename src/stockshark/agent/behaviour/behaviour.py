from abc import ABC, abstractmethod
from typing import Optional

from stockshark.chess_engine.chess_engine import ChessEngine


class Behaviour(ABC):

    @abstractmethod
    def gen_move(self, engine: ChessEngine) -> Optional[str]:
        pass
