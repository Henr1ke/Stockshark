import time
from typing import Optional

import cv2
import numpy as np
from numpy import ndarray

from chess.adb.daoADB import DaoADB
from chess.chessGame.chessGame import ChessGame
from chess.img_process.identifier import Identifier
from chess.img_process.image_funcs import ImageFuncs
from chess.util.move import Move
import constants
from chess.util.position import Position


class MobileChess:
    def __init__(self, dao_adb: DaoADB) -> None:
        self.__dao_adb: DaoADB = dao_adb
        self.__is_white: bool = self.__is_white()

    @property
    def is_white(self) -> bool:
        return self.__is_white

    def __is_white(self) -> bool:
        white_king = Identifier.read_img("chess_components",
                                         "white_king")  # cv2.imread('../images/chess_components/white_king.png')
        black_king = Identifier.read_img("chess_components",
                                         "black_king")  # cv2.imread('../images/chess_components/black_king.png')
        kings = white_king, black_king

        self.__dao_adb.screenshot()
        screenshot = Identifier.read_last_screenshot()
        board = ImageFuncs.crop(screenshot, *constants.BOARD_COORDS_BOT)
        board_gray = ImageFuncs.grayscale(board)
        board_grad = ImageFuncs.morph_grad(board_gray)

        kings_gray = [ImageFuncs.grayscale(img) for img in kings]
        kings_grad = [ImageFuncs.morph_grad(img) for img in kings_gray]

        kings_rects = [Identifier.find_template(board_grad, img) for img in kings_grad]
        kings_colors = Identifier.match_colors(board_gray, kings_gray, kings_rects)
        kings_color_rects = Identifier.match_color_rect(kings_rects, kings_colors)
        wk, bk = kings_color_rects[0][0], kings_color_rects[1][0]
        return wk[1] > bk[1]

    def play(self, move: Move) -> None:
        board_coords = Identifier.get_board_coords()
        botleft_corner = (board_coords[0], board_coords[1] + board_coords[3])
        gap = board_coords[2] / 8

        for pos in (move.start_pos, move.end_pos):
            x = int(botleft_corner[0] + gap * pos.col + gap / 2)
            y = int(botleft_corner[1] - gap * pos.row - gap / 2)
            self.__dao_adb.tap_screen(x, y)

    def has_adv_played(self) -> None:
        pass

    def get_w_sel_count(self, tile: ndarray) -> int:
        return Identifier.get_value_count(tile[:, :, 0], Identifier.TILE_W_PLAYED_COLOR)

    def get_b_sel_count(self, tile: ndarray) -> int:
        return Identifier.get_value_count(tile[:, :, 2], Identifier.TILE_B_PLAYED_COLOR)

    def get_adv_move(self, game: ChessGame) -> Move:
        while True:
            selected_move = self.get_selected_move()
            if selected_move is not None:
                played_moves = game.played_moves
                if len(played_moves) == 0 or selected_move != played_moves[-1]:
                    return selected_move

            time.sleep(0.5)

    def get_selected_move(self) -> Optional[Move]:  # TODO fazer o caso em que não há selected move
        self.__dao_adb.screenshot()
        screenshot = Identifier.read_last_screenshot()
        board = ImageFuncs.crop(screenshot, *constants.BOARD_COORDS_BOT)

        start_pos = None
        end_pos = None
        for row_idx in range(8):
            for col_idx in range(8):
                pos = Position(col_idx, row_idx)
                tile = self.get_tile(board, pos)

                if self.is_tile_selected(tile):
                    if self.is_tile_empty(tile):
                        start_pos = pos
                    else:
                        end_pos = pos

                    if start_pos is not None and end_pos is not None:
                        break
            if start_pos is not None and end_pos is not None:
                break

        if start_pos is None or end_pos is None:
            return None

        return Move(start_pos, end_pos)

    def get_tile(self, board: ndarray, pos: Position) -> ndarray:
        side_len = board.shape[0] / 8
        margin = 10  # pixel

        x = pos.col if self.__is_white else 7 - pos.col
        y = pos.row if self.__is_white else 7 - pos.row

        x1 = int(x * side_len + margin)
        x2 = int((x + 1) * side_len - margin)
        y1 = int(board.shape[0] - (y + 1) * side_len + margin)
        y2 = int(board.shape[0] - y * side_len - margin)

        return ImageFuncs.crop(board, x1, y1, x2, y2)

    def is_tile_selected(self, tile: ndarray) -> bool:
        thresh_val = tile.shape[0] * tile.shape[1] * 0.02  # 2% of all tile pixels
        # Identifier.debug_show_img(tile)
        w_sel_count = self.get_w_sel_count(tile)
        b_sel_count = self.get_b_sel_count(tile)
        return w_sel_count > thresh_val or b_sel_count > thresh_val

    def is_tile_empty(self, tile: ndarray) -> bool:  # TODO tweakar isto
        thresh_val = 20  # 95% of all tile pixels
        gs = ImageFuncs.grayscale(tile)
        std = np.std(gs)
        print(std)
        return std < thresh_val

if __name__ == "__main__":
    dao = DaoADB()
    dao.connect()
    mc = MobileChess(dao)
    b = mc.get_selected_move()
    print(b)
