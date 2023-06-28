import os
import pathlib

import cv2
import numpy as np

from stockshark.art_vis.detector import Detector
from stockshark.art_vis.image_processing import ImageProcessing
from stockshark.util.tile import Tile


def gen_mean_pieces():
    for piece_name in ("pawn", "knight", "bishop", "rook", "queen", "king"):
        w_p = ImageProcessing.read_img(f"chess_components/w_{piece_name}.png")
        b_p = ImageProcessing.read_img(f"chess_components/b_{piece_name}.png")

        max_w = max(w_p.shape[1], b_p.shape[1])
        max_h = max(w_p.shape[0], b_p.shape[0])

        w_p_r = ImageProcessing.resize(w_p, (max_w, max_h))
        b_p_r = ImageProcessing.resize(b_p, (max_w, max_h))

        combined = ImageProcessing.combine_imgs(w_p_r, b_p_r)

        ImageProcessing.show(combined, f"m_{piece_name}")


def gen_grad_pieces():
    for piece_name in ("pawn", "knight", "bishop", "rook", "queen", "king"):
        p = ImageProcessing.read_img(f"chess_components/m_{piece_name}.png")
        p_bw = ImageProcessing.grayscale(p)
        p_grad = ImageProcessing.morph_grad(p_bw)
        ImageProcessing.show(p_grad, f"g_{piece_name}")


def get_piece_in_tile():
    screenshot = ImageProcessing.read_img(f"screenshots/screenshot.png")
    board_info = Detector.find_board(screenshot)
    if board_info is None:
        return
    board, _ = board_info
    detector = Detector(board)

    piece_names = (Detector.KNIGHT, Detector.BISHOP, Detector.ROOK, Detector.QUEEN)

    tiles = [
        Tile("f8"),
        Tile("c8"),
        Tile("b8"),
        Tile("d7"),
        Tile("d8")
    ]

    for tile in tiles:
        coord = detector.tile_to_coord(tile)
        tile_img = Detector.get_tile_img(board, coord)
        print(tile)

        if detector.is_tile_empty(tile_img):
            print("Empty")

        tile_grayscale = ImageProcessing.grayscale(tile_img)
        tile_grad = ImageProcessing.morph_grad(tile_grayscale)
        ImageProcessing.show(tile_grad)

        diffs = []
        for piece_name in piece_names:
            piece_grad = ImageProcessing.read_img(f"chess_components/g_{piece_name}.png", is_grayscale=True)
            piece_resized = ImageProcessing.resize(piece_grad, tile_grad.shape)
            diff = np.sum(tile_grad != piece_resized)
            diffs.append(diff)

        print(diffs)
        print(piece_names[np.argmin(diffs)])
        print()


def identify_board():
    current_path = pathlib.Path(__file__).parent.resolve()
    dir = f"{current_path}/../../images/screenshots"
    for img_name in (os.listdir(dir)):
        screenshot = ImageProcessing.read_img(f"screenshots/{img_name}")

        scn_gray = ImageProcessing.grayscale(screenshot)
        scn_w = screenshot.shape[1]

        empty_board = ImageProcessing.read_img("chess_components/empty_board.png")
        eb_resized = cv2.resize(empty_board, (scn_w, scn_w), interpolation=cv2.INTER_AREA)
        empty_board_gray = ImageProcessing.grayscale(eb_resized)

        positions = ImageProcessing.locate(scn_gray, empty_board_gray)
        if len(positions) == 1:
            pos = positions[0]

            scn_w = screenshot.shape[1]

            start_point = (0, int(pos[1] - scn_w / 2))
            end_point = (scn_w, int(pos[1] + scn_w / 2))
            cv2.rectangle(screenshot, start_point, end_point, 128, 10)

            scaled_img = ImageProcessing.scale(screenshot, 0.5)
            ImageProcessing.show(scaled_img, img_name)


def identify_pieces():
    scrn_img = ImageProcessing.read_img("screenshots/Screenshot.png")
    board_info = Detector.find_board(scrn_img)
    if board_info is None:
        exit()

    b_img, _ = board_info
    b_gray = ImageProcessing.grayscale(b_img)
    b_grad = ImageProcessing.morph_grad(b_gray)

    for piece_name in ("pawn", "knight", "bishop", "rook", "queen", "king"):
        p_img = ImageProcessing.read_img(f"chess_components/m_{piece_name}.png")
        p_gray = ImageProcessing.grayscale(p_img)
        p_grad = ImageProcessing.morph_grad(p_gray)

        print()
        print(piece_name)

        positions = ImageProcessing.locate(b_grad, p_grad, margin=12)
        print(positions)

        half_shape = np.array(p_grad.shape)[::-1] / 2
        b_copy = b_img.copy()
        for pos in positions:
            start_point = np.array(pos - half_shape, dtype=int)
            end_point = np.array(pos + half_shape, dtype=int)
            cv2.rectangle(b_copy, start_point, end_point, 128, 4)
        ImageProcessing.show(b_copy, piece_name)
        ImageProcessing.write_img(f"debug/select_pieces/{piece_name}.png", b_copy)


if __name__ == '__main__':
    get_piece_in_tile()
    pass
