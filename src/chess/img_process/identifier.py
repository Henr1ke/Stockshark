from typing import List, Tuple

import cv2
import numpy as np
from numpy import ndarray

from chess.img_process.image_funcs import ImageFuncs
import pathlib


class Identifier:
    PIECE_W_COLOR: int = 248
    PIECE_B_COLOR: int = 84

    TILE_W_COLOR: int = 235
    TILE_B_COLOR: int = 133

    """ Blue filter """
    TILE_W_PLAYED_COLOR: int = 131

    """ Red filter """
    TILE_B_PLAYED_COLOR: int = 187

    @staticmethod
    def find_template(img: ndarray, template: ndarray, thrs=0.55) -> ndarray:
        # Este método apenas dá atenção ao formato da peça, não interessa a cor
        result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

        ys, xs = (result >= thrs).nonzero()
        overlapping_boxes = [(x, y, template.shape[1], template.shape[0]) for x, y in zip(xs, ys)]

        # Group overlapping rectangles as one
        template_boxes, _ = cv2.groupRectangles(overlapping_boxes, 1, 1)
        return template_boxes

    # Todo receber a screenshot e o objeto Coordinates, fazer crop, chamar o save_fen_str() e retornar a crop
    @staticmethod
    def get_board_coords(screen: ndarray = cv2.imread('../../images/screenshots/Screenshot_1.png'),
                         board: ndarray = cv2.imread('../../images/chess_components/empty_board.png')):
        return Identifier.find_template(screen, board, thrs=0.4)[0]

    # TODO fazer o save_fen_str(board:ndarray) -> None: (obtem a fen_str, verifica se ja existe e guarda a img na pasta fen_strings)

    @staticmethod
    def is_piece_white(piece_img: ndarray) -> bool:
        w_pixel_count = np.sum(piece_img == Identifier.PIECE_W_COLOR)
        b_pixel_count = np.sum(piece_img == Identifier.PIECE_B_COLOR)
        return w_pixel_count >= b_pixel_count

    @staticmethod
    def get_piece_color(board_img: ndarray, piece_img: ndarray, box: ndarray) -> bool:
        x1, x2, y1, y2 = box[0], box[0] + box[2], box[1], box[1] + box[3]
        crop = ImageFuncs.crop(board_img, x1, y1, x2, y2)
        diff = cv2.absdiff(piece_img, crop)
        avg_diff = cv2.mean(diff)[0] / 255
        return avg_diff < 0.3

    @staticmethod
    def match_colors(board_img: ndarray, piece_imgs: List[ndarray], rects: List[List[ndarray]]) -> List:
        pairs = zip(piece_imgs, rects)
        return [[Identifier.get_piece_color(board_img, img, r) for r in rect] for img, rect in pairs]

    # @staticmethod
    # def match_colors(board_img: ndarray, piece_img: ndarray, boxes: ndarray) -> List[bool]:
    #     return [Identifier.get_piece_color(board_img, piece_img, box) for box in boxes]

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

    @staticmethod
    def get_value_count(img: ndarray, value: int) -> int:
        return int(np.sum(img == value))

    @staticmethod
    def read_img(folder: str, filename: str) -> ndarray:
        current_path = pathlib.Path(__file__).parent.resolve()
        return cv2.imread(f"{current_path}/../../images/{folder}/{filename}.png")

    @staticmethod
    def read_last_screenshot():
        return Identifier.read_img("screenshots", "Screenshot")

    @staticmethod
    def debug_show_img(img: ndarray, title: str = "debug") -> None:
        cv2.imshow(title, img)
        cv2.waitKey()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    scr1 = cv2.imread('../../images/screenshots/Screenshot_getadvmove.png')

    crop = ImageFuncs.crop(scr1, 0, 625, 1080, 1705)[:, :, 0]
    crop = ImageFuncs.scale(crop)
    print(Identifier.get_value_count(crop, Identifier.TILE_W_PLAYED_COLOR))
    cv2.imshow("Red filter", crop)
    cv2.waitKey()
    cv2.destroyAllWindows()
