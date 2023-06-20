import time
from typing import Tuple, Optional

from numpy import ndarray

from stockshark.adb.dao_adb import DaoADB
from stockshark.chess_engine.game import Game
from stockshark.util.move import Move
from stockshark.art_vis.detector import Detector


class MobilePlayer:
    WAIT_TIME = 0.5

    def __init__(self, dao_adb: DaoADB, initial_board: ndarray, board_center: Tuple[int, int]) -> None:
        self.__dao_adb: DaoADB = dao_adb
        self.__detector: Detector = Detector(initial_board)
        self.__on_white_side: bool = self.__detector.on_white_side

        self.__board_tl_corner: Tuple[int, int] = (
            int(board_center[0] - self.__detector.board_w / 2), int(board_center[1] - self.__detector.board_w / 2))

    @property
    def on_white_side(self) -> bool:
        return self.__on_white_side

    def play(self, move: Move) -> None:
        for pos in (move.start_tile, move.end_tile):
            x, y = self.__detector.pos_to_loc(pos)
            self.__dao_adb.tap_screen(self.__board_tl_corner[0] + x, self.__board_tl_corner[1] + y)
            time.sleep(MobilePlayer.WAIT_TIME)

    def get_adv_move(self, game: Game) -> Optional[Move]:
        while True:
            screenshot = self.__dao_adb.screenshot()
            board_info = Detector.find_board(screenshot, self.__detector)
            if board_info is None:
                return None
            board, _ = board_info
            selected_move = self.__detector.get_selected_move(board)
            if selected_move is not None:
                played_moves = game.played_moves
                if len(played_moves) == 0 or selected_move != played_moves[-1]:
                    return selected_move

            time.sleep(0.5)
