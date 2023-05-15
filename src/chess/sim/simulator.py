from abc import ABC, abstractmethod
from typing import Optional

from chess.chessGame.chessGame import ChessGame
from chess.chessGame.state import State
from chess.sim.visualizer import Visualizer


class Simulator(ABC):
    def __init__(self, game: ChessGame, vis: Optional[Visualizer] = None):
        self._game = game
        self._vis = vis

    def execute(self) -> None:
        while self._game.state == State.IN_PROGRESS:
            if self._vis is not None:
                self._vis.show(self._game)

            self._update_game()
        if self._vis is not None:
            self._vis.show(self._game)

    @abstractmethod
    def _update_game(self):
        pass
