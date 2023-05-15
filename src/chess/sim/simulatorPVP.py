from abc import ABC
from typing import Optional

from chess.chessGame.chessGame import ChessGame
from chess.player.player import Player
from chess.sim.simulator import Simulator
from chess.sim.visualizer import Visualizer


class SimulatorPVP(Simulator, ABC):
    def __init__(self, player_w: Player, player_b: Player, game: ChessGame, vis: Optional[Visualizer]) -> None:
        super().__init__(game, vis)
        self._player_w: Player = player_w
        self._player_b: Player = player_b

    def _update_game(self) -> None:
        player = self._player_w if self._game.is_white_turn else self._player_b
        move = player.gen_move(self._game)
        self._game.play(move)
