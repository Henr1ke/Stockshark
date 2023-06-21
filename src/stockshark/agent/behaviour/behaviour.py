from abc import ABC, abstractmethod
from typing import Optional

from stockshark.chess_engine.game_engine import GameEngine
from stockshark.util.move import Move


class Behaviour(ABC):

    @abstractmethod
    def gen_move(self, game: GameEngine) -> Optional[Move]:
        pass
