from typing import Optional

from chess.adb.dao_adb import DaoADB
from chess.adb.mobile_chess import MobileChess
from chess.art_vis.detector import Detector
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
        self._on_white_side: bool = mobile.on_white_side

    def _update_game(self) -> bool:
        if self._game.is_white_turn == self._on_white_side:
            move = self._player.gen_move(self._game)
            sucess = self._game.play(move)
            if sucess:
                self._mobile.play(move)

        else:
            move = self._mobile.get_adv_move(self._game)
            if move is None:
                return False

            self._game.play(move)

        return True


if __name__ == '__main__':
    d = DaoADB()
    d.connect()

    screenshot = d.screenshot()
    board_info = Detector.find_board(screenshot)
    if board_info is None:
        exit()

    board, center = board_info

    m = MobileChess(d, board, center)

    g = ChessGame()

    v = Visualizer(Visualizer.CHARSET_LETTER)

    simulator = SimulatorADB(PlayerRandom(), m, g, v)
    simulator.execute()
