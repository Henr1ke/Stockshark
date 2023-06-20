from abc import ABC, abstractmethod
from typing import Optional

from stockshark.chess_engine.game_engine import GameEngine
from stockshark.chess_engine.state import State
from stockshark.sim.visualizer import Visualizer


class Simulator(ABC):
    def __init__(self, game: GameEngine, vis: Optional[Visualizer] = None) -> None:
        self._game = game
        self._vis = vis

    def execute(self) -> None:
        while self._game.state == State.IN_PROGRESS:
            if self._vis is not None:
                self._vis.show(self._game)

            sucess = self._update_game()
            if not sucess:
                break

        if self._vis is not None:
            self._vis.show(self._game)

    @abstractmethod
    def _update_game(self) -> bool:
        pass
