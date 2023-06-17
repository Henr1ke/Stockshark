from abc import ABC
from typing import Optional

from stockshark.chess_engine.game import Game
from stockshark.player.player import Player
from stockshark.player.player_random import PlayerRandom
from stockshark.sim.simulator import Simulator
from stockshark.sim.visualizer import Visualizer


class SimulatorPVP(Simulator, ABC):
    def __init__(self, player_w: Player, player_b: Player, game: Game, vis: Optional[Visualizer]) -> None:
        super().__init__(game, vis)
        self._player_w: Player = player_w
        self._player_b: Player = player_b

    def _update_game(self) -> bool:
        player = self._player_w if self._game.is_white_turn else self._player_b
        move = player.gen_move(self._game)
        self._game.play(move)
        return True


if __name__ == '__main__':
    game = Game()
    player_w = PlayerRandom()
    player_b = PlayerRandom()
    visualizer = Visualizer(Visualizer.CHARSET_LETTER)

    simulator = SimulatorPVP(player_w, player_b, game, visualizer)
    simulator.execute()
