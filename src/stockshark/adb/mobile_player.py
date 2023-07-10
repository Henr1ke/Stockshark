import time
from typing import Tuple, Optional

from numpy import ndarray

from stockshark.adb.dao_adb import DaoADB
from stockshark.art_vis.detector import Detector
from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.piece.piece import Piece


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

    def play(self, move: str) -> None:
        start_tile = move[:2]
        end_tile = move[2:4]
        for tile in (start_tile, end_tile):
            x, y = self.__detector.tile_to_coord(tile)
            self.__dao_adb.tap_screen(self.__board_tl_corner[0] + x, self.__board_tl_corner[1] + y)
            time.sleep(MobilePlayer.WAIT_TIME)

    def get_adv_move(self, engine: ChessEngine) -> Optional[str]:
        while True:
            screenshot = self.__dao_adb.screenshot()
            board_info = Detector.find_board(screenshot, self.__detector)
            if board_info is None:
                return None
            board, _ = board_info
            sel_move = self.__detector.get_selected_move(board)

            if sel_move is not None:
                if self.__is_promotion_move(engine, sel_move):
                    end_tile = sel_move[2:4]
                    piece_type = self.__detector.get_piece_at_tile(board, end_tile).lower()
                    if piece_type is not None:
                        sel_move = sel_move + piece_type

                played_moves = engine.played_moves
                if len(played_moves) == 0 or sel_move != played_moves[-1][:4]:
                    return sel_move

            time.sleep(0.5)

    @staticmethod
    def __is_promotion_move(engine: ChessEngine, move: str) -> bool:
        start_tile = move[:2]
        end_tile = move[2:4]
        piece = engine.get_piece_at(start_tile)
        return piece is not None and piece.lower() == Piece.PAWN_B and \
            (start_tile[1] == ('7' if piece.isupper() else '2')) and \
            (end_tile[1] == ('8' if piece.isupper() else '1'))





