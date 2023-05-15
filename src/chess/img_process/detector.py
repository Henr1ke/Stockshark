from typing import List
import numpy as np
from numpy import ndarray

from chess.img_process.process_image import ProcessImage
from chess.img_process.identifier import Identifier
from chess.img_process.visualizer import Visualizer


class Detector:
    @staticmethod
    def detect_pieces(screenshot: ndarray, piece_imgs: List[ndarray]):
        screenshot_gray = ProcessImage.grayscale_img(screenshot)
        screenshot_grad = ProcessImage.morph_grad_img(screenshot_gray)

        piece_imgs_gray = [ProcessImage.grayscale_img(img) for img in piece_imgs]
        piece_imgs_grad = [ProcessImage.morph_grad_img(img) for img in piece_imgs_gray]

        board_img, corners = ProcessImage.crop_board(screenshot_grad, piece_imgs_grad[-1])
        add_board = np.hstack((corners[:2], [0, 0]))
        rects = [Identifier.find_template(board_img, img) for img in piece_imgs_grad]
        """ Adicionar a posição da board na screenshot original para os quadrados ficarem alinhados"""
        rects = [[r + add_board for r in rect] for rect in rects]
        rects[-1] = [corners]

        colors_list = Identifier.match_colors(screenshot_gray, piece_imgs_gray, rects)
        matching_color_rects = Identifier.match_color_rect(rects, colors_list)
        Visualizer.draw_results_squares(screenshot, matching_color_rects)
        piece_coordinate_dict = Identifier.determine_pieces_squares(matching_color_rects)
        FEN = Detector.fen_string(piece_coordinate_dict)
        return FEN

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


if __name__ == "__main__":
    import cv2

    scr = cv2.imread('../chessPiecesImg/Screenshot_1.png')
    piece_images = [
        cv2.imread('../chessPiecesImg/white_pawn.png'),
        cv2.imread('../chessPiecesImg/white_rook.png'),
        cv2.imread('../chessPiecesImg/white_bishop.png'),
        cv2.imread('../chessPiecesImg/white_knight.png'),
        cv2.imread('../chessPiecesImg/white_king.png'),
        cv2.imread('../chessPiecesImg/white_queen.png'),
        cv2.imread('../chessPiecesImg/black_pawn.png'),
        cv2.imread('../chessPiecesImg/black_rook.png'),
        cv2.imread('../chessPiecesImg/black_bishop.png'),
        cv2.imread('../chessPiecesImg/black_knight.png'),
        cv2.imread('../chessPiecesImg/black_king.png'),
        cv2.imread('../chessPiecesImg/black_queen.png'),
        cv2.imread('../chessPiecesImg/screenshot_emptyboard.png')
    ]
    fen_str = Detector.detect_pieces(scr, piece_images)
    print(fen_str)
    cv2.imshow('Result', scr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
