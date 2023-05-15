from typing import Optional

from chess.adb.mobileChess import MobileChess
from chess.chessGame.chessGame import ChessGame
from chess.player.player import Player
from chess.sim.simulator import Simulator
from chess.sim.visualizer import Visualizer


class SimulatorADB(Simulator):
    def __init__(self, player: Player, mobile: MobileChess, game: ChessGame, vis: Optional[Visualizer]) -> None:
        super().__init__(game, vis)
        self.__player: Player = player
        self.__mobile: MobileChess = mobile
        self.__is_white: bool = mobile.is_white()

    def _update_game(self):
        pass
