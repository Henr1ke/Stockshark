import time
from typing import Optional

import numpy as np
from numpy import ndarray

from chess.adb.coordinates.coordinates import Coordinates
from chess.adb.daoADB import DaoADB
from chess.chessGame.chessGame import ChessGame
from chess.img_process.identifier import Identifier
from chess.img_process.image_funcs import ImageFuncs
from chess.sim.visualizer import Visualizer
from chess.util.move import Move
from chess.util.position import Position
import cv2

class MobileChess:
    def __init__(self, dao_adb: DaoADB, coordinates: Coordinates, is_vs_bot: bool) -> None:
        self.__dao_adb: DaoADB = dao_adb
        self.__coordinates: Coordinates = coordinates
        self.__is_vs_bot: bool = is_vs_bot
        self.__plays_as_whites: bool = self.__is_playing_as_whites()

    @property
    def plays_as_whites(self) -> bool:
        return self.__plays_as_whites

    def __is_playing_as_whites(self) -> bool:
        white_king = Identifier.read_img("chess_components",
                                         "white_king")  # cv2.imread('../images/chess_components/white_king.png')
        black_king = Identifier.read_img("chess_components",
                                         "black_king")  # cv2.imread('../images/chess_components/black_king.png')
        kings = white_king, black_king

        board_width = self.__coordinates.board_width()
        x1, y1 = self.__coordinates.board_tl_corner_coords_bot() if self.__is_vs_bot \
            else self.__coordinates.board_tl_corner_coords_player()
        x2, y2 = x1 + board_width, y1 + board_width

        self.__dao_adb.screenshot()
        screenshot = Identifier.read_last_screenshot()
        board = ImageFuncs.crop(screenshot, x1, y1, x2, y2)

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
        topleft_corner = self.__coordinates.board_tl_corner_coords_bot() if self.__is_vs_bot \
            else self.__coordinates.board_tl_corner_coords_bot()

        for pos in (move.start_pos, move.end_pos):
            x, y = self.__coordinates.pos_coords(pos, self.__plays_as_whites, topleft_corner)
            self.__dao_adb.tap_screen(x, y)

    def get_adv_move(self, game: ChessGame) -> Move:
        while True:
            selected_move = self._get_selected_move()
            if selected_move is not None:
                played_moves = game.played_moves
                if len(played_moves) == 0 or selected_move != played_moves[-1]:
                    return selected_move

            time.sleep(0.5)

    @staticmethod
    def _get_w_sel_count(tile: ndarray) -> int:
        return Identifier.get_value_count(tile[:, :, 0], Identifier.TILE_W_PLAYED_COLOR)

    @staticmethod
    def _get_b_sel_count(tile: ndarray) -> int:
        return Identifier.get_value_count(tile[:, :, 2], Identifier.TILE_B_PLAYED_COLOR)

    def _get_selected_move(self) -> Optional[Move]:
        board_width = self.__coordinates.board_width()
        x1, y1 = self.__coordinates.board_tl_corner_coords_bot() if self.__is_vs_bot \
            else self.__coordinates.board_tl_corner_coords_bot()
        x2, y2 = x1 + board_width, y1 + board_width

        self.__dao_adb.screenshot()
        screenshot = Identifier.read_last_screenshot()
        board = ImageFuncs.crop(screenshot, x1, y1, x2, y2)

        start_pos = None
        end_pos = None
        for row_idx in range(8):
            for col_idx in range(8):
                pos = Position(col_idx, row_idx)
                tile = self._get_tile(board, pos)

                if self._is_tile_selected(tile):
                    if self._is_tile_empty(tile):
                        if start_pos is not None:
                            # Two empty selected tiles found, it's a castle movve
                            return self._get_castle_move(start_pos, pos)
                        else:
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

    def _get_tile(self, board: ndarray, pos: Position) -> ndarray:
        side_len = board.shape[0] / 8
        margin = 10  # pixel

        x = pos.col if self.__plays_as_whites else 7 - pos.col
        y = pos.row if self.__plays_as_whites else 7 - pos.row

        x1 = int(x * side_len + margin)
        x2 = int((x + 1) * side_len - margin)
        y1 = int(board.shape[0] - (y + 1) * side_len + margin)
        y2 = int(board.shape[0] - y * side_len - margin)

        return ImageFuncs.crop(board, x1, y1, x2, y2)

    def _is_tile_selected(self, tile: ndarray) -> bool:
        thresh_val = tile.shape[0] * tile.shape[1] * 0.02  # 2% of all tile pixels
        # Identifier.debug_show_img(tile)
        w_sel_count = self._get_w_sel_count(tile)
        b_sel_count = self._get_b_sel_count(tile)
        return w_sel_count > thresh_val or b_sel_count > thresh_val

    @staticmethod
    def _is_tile_empty(tile: ndarray) -> bool:
        thresh_val = 20
        gs = ImageFuncs.grayscale(tile)
        std = np.std(gs)
        return std < thresh_val

    @staticmethod
    def _get_castle_move(pos1: Position, pos2: Position) -> Optional[Move]:
        if pos1.row != pos2.row or pos1.row != 0 and pos1.row != 7:
            return None

        start_pos, other_pos = (pos1, pos2) if pos1.col == 4 else (pos2, pos1)
        end_pos = Position(2 if other_pos.col == 0 else 6, start_pos.row)

        return Move(start_pos, end_pos)


# if __name__ == "__main__":
#     dao = DaoADB()
#     dao.connect()
#     mc = MobileChess(dao)
#     game = ChessGame()
#     vis = Visualizer(Visualizer.W_PIECE_CHARSET_LETTER, Visualizer.B_PIECE_CHARSET_LETTER)
#
#     game.play(Move(Position("a2"), Position("a4")))
#     vis.show(game)
#     game.play(Move(Position("a7"), Position("a5")))
#     vis.show(game)
#     game.play(Move(Position("b2"), Position("b4")))
#     vis.show(game)
#     ti = time.time()
#     move = mc.get_adv_move(game)
#     print(time.time() - ti)
#     game.play(move)
#     vis.show(game)
