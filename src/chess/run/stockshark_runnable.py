import time
from typing import Optional

from chess.adb.coordinates.coordinates import Coordinates
from chess.adb.dao_adb import DaoADB
from chess.adb.menu_navigator import MenuNavigator
from chess.adb.mobile_chess import MobileChess
from chess.art_vis.detector import Detector
from chess.chessGame.chess_game import ChessGame
from chess.player.player import Player
from chess.sim.simulator_adb import SimulatorADB
from chess.sim.visualizer import Visualizer


class StockSharkRunnable:
    def __init__(self, coordinates: Coordinates):
        self.__dao_adb = DaoADB()
        connected = self.__dao_adb.connect()
        if not connected:
            raise RuntimeError("Error connecting to the device")

        self.__coordinates = coordinates
        self.__menu_navigator = MenuNavigator(self.__dao_adb, coordinates)

    def open_app(self):
        self.__menu_navigator.open_app()

    def start_game_computer(self, diff_lvl: int, on_white_side: Optional[bool]):
        self.__menu_navigator.vs_computer(diff_lvl, on_white_side)

    def start_game_friend(self, username: str, on_white_side: Optional[bool], duration: Optional[int]):
        self.__menu_navigator.vs_friend(username, on_white_side, duration)

    def run_game(self, player: Player, show_simulation: bool = True) -> bool:
        board, center = None, None
        for _ in range(60):
            screenshot = self.__dao_adb.screenshot()
            board_info = Detector.find_board(screenshot)
            if board_info is None:
                time.sleep(1)
            else:
                board, center = board_info
                break

        if board is None:
            return False

        mobile_chess = MobileChess(self.__dao_adb, board, center)

        game = ChessGame()
        vis = None if not show_simulation else Visualizer(Visualizer.CHARSET_LETTER)

        simulator = SimulatorADB(player, mobile_chess, game, vis)
        simulator.execute()

        return True
