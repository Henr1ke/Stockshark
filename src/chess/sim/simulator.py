from typing import Optional

from chess.player.player import Player
from chess.sim.game import Game
from chess.sim.gameRules import GameRules
from chess.sim.state import State
from chess.sim.visualizer import Visualizer


class Simulator:
    def __init__(self, game: Game, player_w: Player, player_b: Player, visualizer: Optional[Visualizer] = None):
        self.__game = game
        self.__player_w = player_w
        self.__player_b = player_b
        self.__visualizer = visualizer

    def execute(self) -> None:
        while self.__game.state == State.IN_PROGRESS:
            if self.__visualizer is not None:
                self.__visualizer.show(self.__game)

            player = self.__player_w if self.__game.is_white_turn else self.__player_b
            move = player.gen_move(self.__game)

            self.__game.play(move)

        if self.__visualizer is not None:
            self.__visualizer.show(self.__game)
