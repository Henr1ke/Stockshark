from __future__ import annotations

import os
import pathlib
from typing import Optional, Tuple, List

import cv2
import numpy as np
from numpy import ndarray

from stockshark.art_vis.image_processing import ImageProcessing
from stockshark.util.move import Move
from stockshark.util.position import Position


class Detector:
    W_PIECE_COLOR: int = 248
    B_PIECE_COLOR: int = 84

    W_TILE_SELECTED_COLOR: int = 131
    B_TILE_SELECTED_COLOR: int = 187

    BOARD_MARGIN_FRACT = 0.002
    TILE_MARGIN_FRACT = 0.09

    PAWN = "pawn"
    KNIGHT = "knight"
    BISHOP = "bishop"
    ROOK = "rook"
    QUEEN = "queen"
    KING = "king"

    PIECE_NAME_TO_LETTER = {PAWN: "p", KNIGHT: "n", BISHOP: "b", ROOK: "r", QUEEN: "q", KING: "k"}

    def __init__(self, initial_board: ndarray) -> None:
        on_white_side = Detector.__is_on_white_side(initial_board)
        if on_white_side is None:
            raise ValueError("Couldn't detect the board orientation")

        self.__on_white_side: bool = on_white_side
        self.__board_w: int = initial_board.shape[1]

    @property
    def on_white_side(self) -> bool:
        return self.__on_white_side

    @property
    def board_w(self) -> int:
        return self.__board_w

    @staticmethod
    def find_board(screenshot: ndarray, detector: Optional[Detector] = None) -> Optional[
        Tuple[ndarray], Tuple[int, int]]:
        scn_gray = ImageProcessing.grayscale(screenshot)
        scn_w = screenshot.shape[1]

        empty_board = ImageProcessing.read_img("chess_components/empty_board.png")
        size = (scn_w, scn_w)
        eb_resized = cv2.resize(empty_board, size, interpolation=cv2.INTER_AREA)
        empty_board_gray = ImageProcessing.grayscale(eb_resized)

        margin = int(screenshot.shape[1] * Detector.BOARD_MARGIN_FRACT)
        positions = ImageProcessing.locate(scn_gray, empty_board_gray, margin=margin)
        if len(positions) == 1:
            center = positions[0]
            board = ImageProcessing.get_square(screenshot, center, screenshot.shape[1])
            if detector is not None:
                detector.save_fen_str(board)
            return board, center
        return None, None

    @staticmethod
    def get_piece_locations(board: ndarray, piece_name: str) -> List[Tuple[int, int]]:
        if piece_name not in Detector.PIECE_NAME_TO_LETTER.keys():
            raise ValueError("Piece name is not valid")

        board_gray = ImageProcessing.grayscale(board)
        board_grad = ImageProcessing.morph_grad(board_gray)

        piece = ImageProcessing.read_img(f"chess_components/m_{piece_name}.png")
        size = (int(board.shape[1] / 8), int(board.shape[1] / 8))
        piece_resized = cv2.resize(piece, size, interpolation=cv2.INTER_AREA)
        piece_gray = ImageProcessing.grayscale(piece_resized)
        piece_grad = ImageProcessing.morph_grad(piece_gray)

        margin = int(board.shape[1] / 8 * Detector.TILE_MARGIN_FRACT)
        return ImageProcessing.locate(board_grad, piece_grad, margin=margin)

    @staticmethod
    def __is_on_white_side(board: ndarray) -> Optional[bool]:
        positions = Detector.get_piece_locations(board, Detector.KING)

        lowest_pos = None
        for i, pos in enumerate(positions):
            if lowest_pos is None or pos[1] >= lowest_pos[1]:
                lowest_pos = pos

        if lowest_pos is None:
            return None

        tile = Detector.get_tile(board, lowest_pos)
        return Detector.is_piece_white(tile)

    @staticmethod
    def get_tile(board: ndarray, center: Tuple[int, int]) -> ndarray:
        margin = board.shape[1] / 8 * Detector.TILE_MARGIN_FRACT
        tile_w = board.shape[1] / 8 - 2 * margin
        return ImageProcessing.get_square(board, center, tile_w)

    @staticmethod
    def is_tile_empty(tile: ndarray) -> bool:
        thresh_val = 20
        gs = ImageProcessing.grayscale(tile)
        std = np.std(gs)
        return std < thresh_val

    @staticmethod
    def is_piece_white(tile: ndarray) -> Optional[bool]:
        if Detector.is_tile_empty(tile):
            return None

        w_pixel_count = ImageProcessing.get_value_count(tile, Detector.W_PIECE_COLOR)
        b_pixel_count = ImageProcessing.get_value_count(tile, Detector.B_PIECE_COLOR)
        return w_pixel_count >= b_pixel_count

    @staticmethod
    def is_tile_selected(tile: ndarray) -> bool:
        thresh_val = tile.shape[0] * tile.shape[1] * 0.02  # 2% of all tile pixels
        w_sel_count = ImageProcessing.get_value_count(tile[:, :, 0], Detector.W_TILE_SELECTED_COLOR)
        b_sel_count = ImageProcessing.get_value_count(tile[:, :, 2], Detector.B_TILE_SELECTED_COLOR)
        return w_sel_count > thresh_val or b_sel_count > thresh_val

    @staticmethod
    def get_castle_move(pos1: Position, pos2: Position) -> Optional[Move]:
        if pos1.row != pos2.row or pos1.row != 0 and pos1.row != 7:
            return None

        start_pos, other_pos = (pos1, pos2) if pos1.col == 4 else (pos2, pos1)
        end_pos = Position(2 if other_pos.col == 0 else 6, start_pos.row)

        return Move(start_pos, end_pos)

    def pos_to_loc(self, pos: Position) -> Tuple[int, int]:
        tile_w = self.__board_w / 8
        if not self.__on_white_side:
            pos = -pos

        x = int(tile_w / 2 + tile_w * pos.col)
        y = int(tile_w / 2 + tile_w * (7 - pos.row))
        return x, y

    def loc_to_pos(self, loc: Tuple[int, int]) -> Position:
        col = int(8 * loc[0] / self.__board_w)
        row = 7 - int(8 * loc[1] / self.__board_w)
        pos = Position(col, row)

        if not self.__on_white_side:
            pos = -pos
        return pos

    def get_piece_positions(self, board: ndarray, piece_name: str) -> List[Position]:
        if piece_name not in Detector.PIECE_NAME_TO_LETTER.keys():
            raise ValueError("Piece name is not valid")

        locations = Detector.get_piece_locations(board, piece_name)
        positions = [self.loc_to_pos(loc) for loc in locations]
        return positions

    def get_selected_move(self, board: ndarray) -> Optional[Move]:
        start_pos = None
        end_pos = None
        for row_idx in range(8):
            for col_idx in range(8):
                pos = Position(col_idx, row_idx)
                loc = self.pos_to_loc(pos)
                tile = Detector.get_tile(board, loc)

                if Detector.is_tile_selected(tile):
                    if Detector.is_tile_empty(tile):
                        if start_pos is not None:
                            # Two empty selected tiles found, it's a castle movve
                            return Detector.get_castle_move(start_pos, pos)
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

    def save_fen_str(self, board: ndarray) -> None:
        fen_str = self.gen_fen_str(board)
        fen_str = fen_str.replace("/", ";")
        current_path = pathlib.Path(__file__).parent.resolve()
        filename = f"fen_strings/{fen_str}.png"

        # os.path.exists(filename)

        # alreadyExists = ImageProcessing.read_img(filename) is None
        if not os.path.exists(f"{current_path}/../../images/{filename}"):
            print("fen doesnt exist")
            ImageProcessing.write_img(filename, board)

    def gen_fen_str(self, board: ndarray) -> str:
        pos_to_piece = {}

        for piece_name in Detector.PIECE_NAME_TO_LETTER.keys():
            letter = Detector.PIECE_NAME_TO_LETTER[piece_name]

            piece_positions = self.get_piece_positions(board, piece_name)
            for pos in piece_positions:
                loc = self.pos_to_loc(pos)
                tile = Detector.get_tile(board, loc)
                is_white = Detector.is_piece_white(tile)
                letter_to_add = letter.upper() if is_white else letter
                pos_to_piece[pos] = letter_to_add

        fen_rows = []
        for row_idx in range(7, -1, -1):
            fen_row = ""
            tile_skips = 0
            for col_idx in range(8):
                pos = Position(col_idx, row_idx)
                if pos not in pos_to_piece.keys():
                    tile_skips += 1
                else:
                    if tile_skips > 0:
                        fen_row += str(tile_skips)
                        tile_skips = 0
                    fen_row += pos_to_piece[pos]
            if tile_skips > 0:
                fen_row += str(tile_skips)
            fen_rows.append(fen_row)

        return "/".join(fen_rows)
