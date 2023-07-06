import time
from typing import Tuple, Optional

from numpy import ndarray
from stockshark.chess_engine.game_engine import GameEngine

from stockshark.adb.dao_adb import DaoADB
from stockshark.art_vis.detector import Detector
from stockshark.piece.pawn import Pawn
from stockshark.util.move import Move


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
        for tile in (move.start_tile, move.end_tile):
            x, y = self.__detector.tile_to_coord(tile)
            self.__dao_adb.tap_screen(self.__board_tl_corner[0] + x, self.__board_tl_corner[1] + y)
            time.sleep(MobilePlayer.WAIT_TIME)

    def get_adv_move(self, game: GameEngine) -> Optional[Move]:
        while True:
            screenshot = self.__dao_adb.screenshot()
            board_info = Detector.find_board(screenshot, self.__detector)
            if board_info is None:
                return None
            board, _ = board_info
            sel_move = self.__detector.get_selected_move(board)

            if self.__is_promotion_move(game, sel_move):
                piece_type = self.__detector.get_piece_type(board, sel_move.end_tile)
                if piece_type is not None:
                    sel_move = Move(sel_move.start_tile, sel_move.end_tile, piece_type)

            if sel_move is not None:
                played_moves = game.played_moves
                if len(played_moves) == 0 or sel_move != played_moves[-1]:
                    return sel_move

            time.sleep(0.5)

    @staticmethod
    def __is_promotion_move(game: GameEngine, move: Move) -> bool:
        piece = game.board[move.start_tile]
        return isinstance(piece, Pawn) and \
            move.start_tile.row == (6 if piece.is_white else 1) and \
            move.end_tile.row == (7 if piece.is_white else 0)


