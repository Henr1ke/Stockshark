from __future__ import annotations

import os
import pathlib
from typing import Optional, Tuple, List

import cv2
import numpy as np
from numpy import ndarray

from stockshark.art_vis.image_processing import ImageProcessing


class Detector:
    W_PIECE_COLOR: int = 248
    B_PIECE_COLOR: int = 84

    W_TILE_SELECTED_COLOR: int = 131
    B_TILE_SELECTED_COLOR: int = 187

    BOARD_MARGIN_FRACT = 0.002
    TILE_MARGIN_FRACT = 0.09

    TILE_EMPTY_THRESH = 20

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
    def find_board(screenshot: ndarray, detector: Optional[Detector] = None) -> \
            Optional[Tuple[ndarray], Tuple[int, int]]:
        scn_gray = ImageProcessing.grayscale(screenshot)
        scn_w = screenshot.shape[1]

        empty_board = ImageProcessing.read_img("chess_components/empty_board.png")
        size = (scn_w, scn_w)
        eb_resized = cv2.resize(empty_board, size, interpolation=cv2.INTER_AREA)
        empty_board_gray = ImageProcessing.grayscale(eb_resized)

        margin = int(screenshot.shape[1] * Detector.BOARD_MARGIN_FRACT)
        coordinates = ImageProcessing.locate(scn_gray, empty_board_gray, margin=margin)
        if len(coordinates) == 1:
            center = coordinates[0]
            board = ImageProcessing.get_square(screenshot, center, scn_w)
            if detector is not None:
                detector.save_fen(board)
            return board, center
        return None

    @staticmethod
    def get_piece_coords(board: ndarray, piece_name: str) -> List[Tuple[int, int]]:
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
        coordinates = Detector.get_piece_coords(board, Detector.KING)

        lowest_coord = None
        for i, coord in enumerate(coordinates):
            if lowest_coord is None or coord[1] >= lowest_coord[1]:
                lowest_coord = coord

        if lowest_coord is None:
            return None

        tile_img = Detector.get_tile_img(board, lowest_coord)
        return Detector.is_piece_white(tile_img)

    @staticmethod
    def get_tile_img(board: ndarray, center: Tuple[int, int]) -> ndarray:
        margin = board.shape[1] / 8 * Detector.TILE_MARGIN_FRACT
        tile_w = board.shape[1] / 8 - 2 * margin
        return ImageProcessing.get_square(board, center, tile_w)

    @staticmethod
    def is_tile_empty(tile_img: ndarray) -> bool:
        gs = ImageProcessing.grayscale(tile_img)
        std = np.std(gs)
        return std < Detector.TILE_EMPTY_THRESH

    @staticmethod
    def is_piece_white(tile_img: ndarray) -> Optional[bool]:
        if Detector.is_tile_empty(tile_img):
            return None

        w_pixel_count = ImageProcessing.get_value_count(tile_img, Detector.W_PIECE_COLOR)
        b_pixel_count = ImageProcessing.get_value_count(tile_img, Detector.B_PIECE_COLOR)
        return w_pixel_count >= b_pixel_count

    @staticmethod
    def is_tile_selected(tile_img: ndarray) -> bool:
        thresh_val = tile_img.shape[0] * tile_img.shape[1] * 0.02  # 2% of all tile pixels
        w_sel_count = ImageProcessing.get_value_count(tile_img[:, :, 0], Detector.W_TILE_SELECTED_COLOR)
        b_sel_count = ImageProcessing.get_value_count(tile_img[:, :, 2], Detector.B_TILE_SELECTED_COLOR)
        return w_sel_count > thresh_val or b_sel_count > thresh_val

    @staticmethod
    def get_castle_move(tile1: str, tile2: str) -> Optional[str]:
        if tile1[1] != tile2[1] or tile1[1] != '1' and tile1[1] != '8':
            return None

        start_tile, other_tile = (tile1, tile2) if tile1[0] == 'e' else (tile2, tile1)
        end_tile = ("c" if other_tile[0] == "a" else "h") + start_tile[1]

        return start_tile + end_tile

    def get_piece_type(self, board: ndarray, tile: Tile) -> Optional[str]:
        piece_names = (Detector.KNIGHT, Detector.BISHOP, Detector.ROOK, Detector.QUEEN)
        piece_types = (Move.PROMOTE_N, Move.PROMOTE_B, Move.PROMOTE_R, Move.PROMOTE_Q)

        coord = self.tile_to_coord(tile)
        tile_img = Detector.get_tile_img(board, coord)

        if Detector.is_tile_empty(tile_img):
            return None

        tile_grayscale = ImageProcessing.grayscale(tile_img)
        tile_grad = ImageProcessing.morph_grad(tile_grayscale)

        diffs = []
        for piece_name in piece_names:
            piece_grad = ImageProcessing.read_img(f"chess_components/g_{piece_name}.png", is_grayscale=True)
            piece_resized = ImageProcessing.resize(piece_grad, tile_grad.shape)
            diff = np.sum(tile_grad != piece_resized)
            diffs.append(diff)

        idx = np.argmin(diffs)
        return piece_types[idx]

    def tile_to_coord(self, tile: Tile) -> Tuple[int, int]:
        tile_w = self.__board_w / 8
        if not self.__on_white_side:
            tile = -tile

        x = int(tile_w / 2 + tile_w * tile.col)
        y = int(tile_w / 2 + tile_w * (7 - tile.row))
        return x, y

    def coord_to_tile(self, coord: Tuple[int, int]) -> Tile:
        col = int(8 * coord[0] / self.__board_w)
        row = 7 - int(8 * coord[1] / self.__board_w)
        tile = Tile(col, row)

        if not self.__on_white_side:
            tile = -tile
        return tile

    def get_piece_tiles(self, board: ndarray, piece_name: str) -> List[Tile]:
        if piece_name not in Detector.PIECE_NAME_TO_LETTER.keys():
            raise ValueError("Piece name is not valid")

        coords = Detector.get_piece_coords(board, piece_name)
        tiles = [self.coord_to_tile(coord) for coord in coords]
        return tiles

    def get_selected_move(self, board: ndarray) -> Optional[Move]:
        start_tile = None
        end_tile = None
        for row_idx in range(8):
            for col_idx in range(8):
                tile = Tile(col_idx, row_idx)
                coord = self.tile_to_coord(tile)
                tile_img = Detector.get_tile_img(board, coord)

                if Detector.is_tile_selected(tile_img):
                    if Detector.is_tile_empty(tile_img):
                        if start_tile is not None:
                            # Two empty selected tiles found, it's a castle move
                            return Detector.get_castle_move(start_tile, tile)
                        else:
                            start_tile = tile
                    else:
                        end_tile = tile

                    if start_tile is not None and end_tile is not None:
                        break
            if start_tile is not None and end_tile is not None:
                break

        if start_tile is None or end_tile is None:
            return None

        return Move(start_tile, end_tile)

    def save_fen(self, board: ndarray) -> None:
        fen = self.gen_fen(board)
        fen = fen.replace("/", ";")
        current_path = pathlib.Path(__file__).parent.resolve()
        filename = f"fenings/{fen}.png"

        # os.path.exists(filename)

        # alreadyExists = ImageProcessing.read_img(filename) is None
        if not os.path.exists(f"{current_path}/../../images/{filename}"):
            ImageProcessing.write_img(filename, board)

    def gen_fen(self, board: ndarray) -> str:
        tile_to_piece = {}

        for piece_name in Detector.PIECE_NAME_TO_LETTER.keys():
            letter = Detector.PIECE_NAME_TO_LETTER[piece_name]

            piece_tiles = self.get_piece_tiles(board, piece_name)
            for tile in piece_tiles:
                coord = self.tile_to_coord(tile)
                tile_img = Detector.get_tile_img(board, coord)
                is_white = Detector.is_piece_white(tile_img)
                letter_to_add = letter.upper() if is_white else letter
                tile_to_piece[tile] = letter_to_add

        fen_rows = []
        for row_idx in range(7, -1, -1):
            fen_row = ""
            tile_skips = 0
            for col_idx in range(8):
                tile = Tile(col_idx, row_idx)
                if tile not in tile_to_piece.keys():
                    tile_skips += 1
                else:
                    if tile_skips > 0:
                        fen_row += str(tile_skips)
                        tile_skips = 0
                    fen_row += tile_to_piece[tile]
            if tile_skips > 0:
                fen_row += str(tile_skips)
            fen_rows.append(fen_row)

        return "/".join(fen_rows)
