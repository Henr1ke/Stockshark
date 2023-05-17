from typing import List, Tuple

import cv2
import numpy as np
from numpy import ndarray

from chess.img_process.image_funcs import ImageFuncs


class Identifier:

    @staticmethod
    def find_template(img: ndarray, template: ndarray, thrs=0.55) -> ndarray:
        # Este método apenas dá atenção ao formato da peça, não interessa a cor
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        ys, xs = (result >= thrs).nonzero()
        overlapping_boxes = [(x, y, template.shape[1], template.shape[0]) for x, y in zip(xs, ys)]

        # Group overlapping rectangles as one
        template_boxes, _ = cv2.groupRectangles(overlapping_boxes, 1, 1)
        return template_boxes

    @staticmethod
    def get_board_coords(screen: ndarray = cv2.imread('../../images/screenshots/Screenshot_1.png'),
                         board: ndarray = cv2.imread('../../images/chess_components/empty_board.png')):
        return Identifier.find_template(screen, board, thrs=0.4)[0]

    @staticmethod
    def check_color(board_img: ndarray, piece_img: ndarray, rect: ndarray) -> bool:
        x1, x2, y1, y2 = rect[0], rect[0] + rect[2], rect[1], rect[1] + rect[3]
        crop = ImageFuncs.crop(board_img, x1, y1, x2, y2)

        diff = cv2.absdiff(piece_img, crop)
        avg_diff = cv2.mean(diff)[0] / 255
        return avg_diff < 0.3  # Baixo do limiar é peça preta

    @staticmethod
    def match_colors(board: ndarray, piece_imgs: List[ndarray], rects: List[List[ndarray]]) -> List:
        pairs = zip(piece_imgs, rects)
        return [[Identifier.check_color(board, img, r) for r in rect] for img, rect in pairs]

    @staticmethod
    def match_color_rect(rects: List, colors: List) -> List:
        return [[r for (r, is_matching) in zip(rect, color) if is_matching] for rect, color in zip(rects, colors)]

    @staticmethod
    def determine_pieces_squares(rects):
        # dict = {id_piece : (0,0)} # peça com id x, está na posição (0,0) que é top right
        rects_copy = rects.copy()
        board_rect = rects_copy.pop(-1)[0]
        tl_board = board_rect[:2]
        gap = abs(board_rect[0] - (board_rect[0] + board_rect[2])) / 8
        board_array = [[None for _ in range(8)] for _ in range(8)]
        for i, pieces in enumerate(rects_copy):
            for piece in pieces:
                piece_x1 = piece[0]
                piece_x2 = piece[0] + piece[2]
                piece_y1 = piece[1]
                piece_y2 = piece[1] + piece[3]
                piece_center = (int((piece_x1 + piece_x2) / 2),
                                int((piece_y1 + piece_y2) / 2))
                piece_coord = np.floor((piece_center - tl_board) / gap)
                board_array[int(piece_coord[0])][int(piece_coord[1])] = i + 1

        return np.fliplr(list(zip(*board_array[::-1])))
