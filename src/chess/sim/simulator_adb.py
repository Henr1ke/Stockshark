from typing import Optional

from chess.adb.coordinates.coordinates_pixel_4 import CoordinatesPixel4
from chess.adb.dao_adb import DaoADB
from chess.adb.mobile_chess import MobileChess
from chess.chessGame.chess_game import ChessGame
from chess.player.player import Player
from chess.player.player_random import PlayerRandom
from chess.sim.simulator import Simulator
from chess.sim.visualizer import Visualizer


class SimulatorADB(Simulator):
    def __init__(self, player: Player, mobile: MobileChess, game: ChessGame, vis: Optional[Visualizer]) -> None:
        super().__init__(game, vis)
        self._player: Player = player
        self._mobile: MobileChess = mobile
        self._plays_as_whites: bool = mobile.plays_as_whites

    def _update_game(self) -> None:
        if self._game.is_white_turn == self._plays_as_whites:
            move = self._player.gen_move(self._game)
            sucess = self._game.play(move)
            if sucess:
                self._mobile.play(move)

        else:
            move = self._mobile.get_adv_move(self._game)
            self._game.play(move)


if __name__ == '__main__':
    d = DaoADB()
    d.connect()

    c = CoordinatesPixel4()

    m = MobileChess(d, c, True)

    g = ChessGame()

    v = Visualizer(Visualizer.W_PIECE_CHARSET_LETTER, Visualizer.B_PIECE_CHARSET_LETTER)

    simulator = SimulatorADB(PlayerRandom(), m, g, v)
    simulator.execute()
