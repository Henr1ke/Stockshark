from typing import List, Tuple

import cv2
import numpy as np
from numpy import ndarray
from chess.art_vis.image_processing import ImageProcessing


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
        similarities = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        detected_pixels = similarities >= thrs

        ys, xs = detected_pixels.nonzero()
        overlapping_boxes = [(x, y, template.shape[1], template.shape[0]) for x, y in zip(xs, ys)]

        # Group overlapping rectangles as one
        template_boxes, _ = cv2.groupRectangles(overlapping_boxes, 1, 1)
        return template_boxes

    # Este metodo dá true ou false se a peça dentro do box faz match à piece_img, devia se chamar match_piece
    @staticmethod
    def get_piece_color(board_img: ndarray, piece_img: ndarray, box: ndarray) -> bool:
        x1, x2, y1, y2 = box[0], box[0] + box[2], box[1], box[1] + box[3]
        crop = ImageProcessing.crop(board_img, x1, y1, x2, y2)
        diff = cv2.absdiff(piece_img, crop)
        avg_diff = cv2.mean(diff)[0] / 255
        return avg_diff < 0.3

    # Se calhar devia se chamar match_pieces
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

    # --------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_value_count(img: ndarray, value: int) -> int:
        return int(np.sum(img == value))

    @staticmethod
    def get_board_img(screen: ndarray, topleft_corner: Tuple[int, int], board_width: int) -> ndarray:
        x1, y1 = topleft_corner
        x2, y2 = x1 + board_width, y1 + board_width
        board = ImageProcessing.crop(screen, x1, y1, x2, y2)

        # Identifier.save_fen_str(board)
        return board

    @staticmethod
    def save_fen_str(board_img: ndarray) -> None:
        fen_str = Identifier.gen_fen_str(board_img)
        filename = f"fen_strings/{fen_str}.png"
        alreadyExists = ImageProcessing.read_img(filename) is None
        if alreadyExists:
            ImageProcessing.write_img(filename, fen_str, board_img)

    @staticmethod
    def gen_fen_str(board_img: ndarray) -> str:
        board_gray = ImageProcessing.grayscale(board_img)
        board_grad = ImageProcessing.morph_grad(board_gray)

        piece_imgs = [
            ImageProcessing.read_img("chess_components/white_pawn.png"),
            ImageProcessing.read_img("chess_components/white_rook.png"),
            ImageProcessing.read_img("chess_components/white_bishop.png"),
            ImageProcessing.read_img("chess_components/white_knight.png"),
            ImageProcessing.read_img("chess_components/white_king.png"),
            ImageProcessing.read_img("chess_components/white_queen.png"),
            ImageProcessing.read_img("chess_components/black_pawn.png"),
            ImageProcessing.read_img("chess_components/black_rook.png"),
            ImageProcessing.read_img("chess_components/black_bishop.png"),
            ImageProcessing.read_img("chess_components/black_knight.png"),
            ImageProcessing.read_img("chess_components/black_king.png"),
            ImageProcessing.read_img("chess_components/black_queen.png"),
            ImageProcessing.read_img("chess_components/empty_board.png")
        ]
        piece_imgs_gray = [ImageProcessing.grayscale(img) for img in piece_imgs]
        piece_imgs_grad = [ImageProcessing.morph_grad(img) for img in piece_imgs_gray]

        rects = [Identifier.find_template(board_grad, img) for img in piece_imgs_grad]
        colors_list = Identifier.match_colors(board_gray, piece_imgs_gray, rects)
        matching_color_rects = Identifier.match_color_rect(rects, colors_list)
        piece_coordinate_dict = Identifier.determine_pieces_squares(matching_color_rects)
        fen = Identifier.fen_string(piece_coordinate_dict)
        return fen

    @staticmethod
    def fen_string(board_array):
        n_to_name = {1: "P",  # white_pawn
                     2: "R",  # white_rook
                     3: "B",  # white_bishop
                     4: "N",  # white_knight
                     5: "K",  # white_king
                     6: "Q",  # white_queen
                     7: "p",  # black_pawn
                     8: "r",  # black_rook
                     9: "b",  # black_bishop
                     10: "n",  # black_knight
                     11: "k",  # black_king
                     12: "q"}  # black_queen
        fen_placement_rows = ["" for _ in range(8)]

        for i, row in enumerate(board_array):
            print(i, row)
            fen_placement_row = ""
            tile_skips = 0
            for piece in row:
                if piece is None:
                    tile_skips += 1
                else:
                    if tile_skips > 0:
                        fen_placement_row += str(tile_skips)
                        tile_skips = 0
                    fen_placement_row += n_to_name[piece]

            if tile_skips > 0:
                fen_placement_row += str(tile_skips)
            fen_placement_rows[i] = fen_placement_row

        return "/".join(fen_placement_rows)

    @staticmethod
    def is_piece_white(piece_img: ndarray) -> bool:
        w_pixel_count = np.sum(piece_img == Identifier.PIECE_W_COLOR)
        b_pixel_count = np.sum(piece_img == Identifier.PIECE_B_COLOR)
        return w_pixel_count >= b_pixel_count


if __name__ == "__main__":
    scr1 = cv2.imread('../../images/screenshots/Screenshot_getadvmove.png')

    crop = ImageProcessing.crop(scr1, 0, 625, 1080, 1705)[:, :, 0]
    crop = ImageProcessing.scale(crop)
    print(Identifier.get_value_count(crop, Identifier.TILE_W_PLAYED_COLOR))
    cv2.imshow("Red filter", crop)
    cv2.waitKey()
    cv2.destroyAllWindows()
