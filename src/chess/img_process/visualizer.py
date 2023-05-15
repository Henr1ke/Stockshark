from typing import List

import cv2
from numpy import ndarray


class Visualizer:
    @staticmethod
    def draw_results(img: ndarray, rects: List, i: int):
        n_to_name = ["P",  # white_pawn 0
                     "R",  # white_rook 1
                     "B",  # white_bishop 2
                     "N",  # white_knight 3
                     "K",  # white_king 4
                     "Q",  # white_queen 5
                     "p",  # black_pawn 6
                     "r",  # black_rook 7
                     "b",  # black_bishop 8
                     "n",  # black_knight 9
                     "k",  # black_king 10
                     "q"]  # black_queen 11
        for r in rects:
            cv2.rectangle(img, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (0, 0, 255), 2)
            if i != 12:
                cv2.putText(
                    img, n_to_name[i], (r[0] + 5, r[1] + 25), cv2.FONT_HERSHEY_DUPLEX, 0.9, color=(0, 0, 255),
                    thickness=2)

    @staticmethod
    def draw_results_squares(board_img: ndarray, rects: List[List[ndarray]]):
        for i, rect in enumerate(rects):
            Visualizer.draw_results(board_img, rect, i)
