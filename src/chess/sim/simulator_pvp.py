from abc import ABC
from typing import Optional

from chess.chessGame.chess_game import ChessGame
from chess.player.behaviour.eat_behaviour import EatBehaviour
from chess.player.behaviour.random_behaviour import RandomBehaviour
from chess.player.player import Player
from chess.player.player_human import PlayerHuman
from chess.player.player_random import PlayerRandom
from chess.player.player_reactive import PlayerReactive
from chess.sim.simulator import Simulator
from chess.sim.visualizer import Visualizer


class SimulatorPVP(Simulator, ABC):
    def __init__(self, player_w: Player, player_b: Player, game: ChessGame, vis: Optional[Visualizer]) -> None:
        super().__init__(game, vis)
        self._player_w: Player = player_w
        self._player_b: Player = player_b

    def _update_game(self) -> bool:
        player = self._player_w if self._game.is_white_turn else self._player_b
        move = player.gen_move(self._game)
        self._game.play(move)
        return True


if __name__ == '__main__':
    game = ChessGame()
    player_w = PlayerRandom()
    player_b = PlayerReactive([EatBehaviour(), RandomBehaviour()])
    visualizer = Visualizer(Visualizer.W_PIECE_CHARSET_LETTER, Visualizer.B_PIECE_CHARSET_LETTER)

    simulator = SimulatorPVP(player_w, player_b, game, visualizer)
    simulator.execute()
