from typing import List

import cv2
import numpy as np
from numpy import ndarray


class Identifier:
    @staticmethod
    def find_template(board: ndarray, piece: ndarray, thrs=0.55):
        # Este método apenas dá atenção ao formato da peça, não interessa a cor
        rects = []
        w, h = piece.shape[1], piece.shape[0]
        res = cv2.matchTemplate(board, piece, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= thrs)

        for pt in zip(*loc[::-1]):
            rects.append((pt[0], pt[1], w, h))
            # cv2.rectangle(board, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 255, 126), -1)

        # Perform a simple non-max suppression
        rects, _ = cv2.groupRectangles(rects, 1, 1)

        return rects

    @staticmethod
    def get_board_coords(screen: ndarray = cv2.imread('chessPiecesImg/Screenshot_1.png'),
                         board: ndarray = cv2.imread('chessPiecesImg/screenshot_emptyboard.png')):
        return Identifier.find_template(screen, board, thrs=0.01)[0]

    @staticmethod
    def check_color(board_img: ndarray, piece_img: ndarray, rect: ndarray) -> bool:
        x0, x1, y0, y1 = rect[0], rect[0] + rect[2], rect[1], rect[1] + rect[3]
        # Dá crop na board apenas no lugar da peça
        crop = (board_img[y0: y1, x0: x1]).copy()

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
