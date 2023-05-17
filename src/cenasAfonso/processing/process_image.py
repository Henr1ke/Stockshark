from typing import Tuple, List

import cv2
import numpy as np
from numpy import ndarray
from cenasAfonso.identifier.identifier import Identifier


class ProcessImage:
    @staticmethod
    def grayscale_img(img: ndarray) -> ndarray:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def morph_grad_img(img: ndarray) -> ndarray:
        s = 3
        kernel = np.ones((s, s), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

    @staticmethod
    def crop_board(screen: ndarray = cv2.imread('../chessPiecesImg/Screenshot_1.png'),
                   board: ndarray = cv2.imread('../chessPiecesImg/screenshot_emptyboard.png')) \
            -> Tuple[ndarray, List[int]]:
        board_coords = Identifier.get_board_coords(screen, board)
        x0, x1, y0, y1 = board_coords[0], board_coords[0] + board_coords[2], board_coords[1], board_coords[1] + \
                                          board_coords[3]
        screen_cropped = (screen[y0: y1, x0: x1]).copy()

        return screen_cropped, board_coords

    @staticmethod
    def resize_img(img: ndarray, scale: float = 0.4) -> ndarray:
        dim = (int(img.shape[1] * scale), int(img.shape[0] * scale))
        return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
