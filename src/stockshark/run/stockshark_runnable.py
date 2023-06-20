import time
from typing import Optional

from stockshark.adb.coordinates.coordinates import Coordinates
from stockshark.adb.dao_adb import DaoADB
from stockshark.adb.menu_navigator import MenuNavigator
from stockshark.adb.mobile_player import MobilePlayer
from stockshark.art_vis.detector import Detector
from stockshark.chess_engine.game_engine import GameEngine
from stockshark.agent.agent import Agent
from stockshark.sim.simulator_adb import SimulatorADB
from stockshark.sim.visualizer import Visualizer


class StockSharkRunnable:
    def __init__(self, coordinates: Coordinates):
        self.__dao_adb = DaoADB()
        connected = self.__dao_adb.connect()
        if not connected:
            raise RuntimeError("Error connecting to the device")

        self.__coordinates = coordinates
        self.__menu_navigator = MenuNavigator(self.__dao_adb, coordinates)

    def open_app(self, wait_time: float = 5):
        self.__menu_navigator.open_app(wait_time)

    def start_game_computer(self, diff_lvl: int, on_white_side: Optional[bool], wait_time: float = 2):
        self.__menu_navigator.vs_computer(diff_lvl, on_white_side, wait_time=wait_time)

    def start_game_friend(self, username: str, on_white_side: Optional[bool], duration: Optional[int],
                          wait_time: float = 2):
        self.__menu_navigator.vs_friend(username, on_white_side, duration, wait_time=wait_time)

    def run_game(self, agent: Agent, show_simulation: bool = True) -> bool:
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

        mobile_chess = MobilePlayer(self.__dao_adb, board, center)

        game = GameEngine()
        vis = None if not show_simulation else Visualizer(Visualizer.CHARSET_LETTER)

        simulator = SimulatorADB(agent, mobile_chess, game, vis)
        simulator.execute()

        return True
