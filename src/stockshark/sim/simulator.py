from abc import ABC, abstractmethod
from typing import Optional

from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.sim.visualizer import Visualizer


class Simulator(ABC):
    def __init__(self, engine: ChessEngine, vis: Optional[Visualizer] = None) -> None:
        self._engine = engine
        self._vis = vis

    def execute(self) -> None:
        while self._engine.state == State.IN_PROGRESS:
            if self._vis is not None:
                self._vis.show(self._engine)

            success = self._update_game()
            if not success:
                break

        if self._vis is not None:
            self._vis.show(self._engine)

    @abstractmethod
    def _update_game(self) -> bool:
        pass
