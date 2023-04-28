from typing import List

import cv2
import numpy as np
from numpy import ndarray


def grayscale_img(img: ndarray) -> ndarray:
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def morph_grad_img(img: ndarray) -> ndarray:
    s = 3
    kernel = np.ones((s, s), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)


def find_template_multiple(board: ndarray, piece: ndarray, threshold=0.55):
    # Este método apenas dá atenção ao formato da peça, não interessa a cor
    rects = []
    w, h = piece.shape[1], piece.shape[0]
    res = cv2.matchTemplate(board, piece, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        rects.append((pt[0], pt[1], w, h))
        # cv2.rectangle(board, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 255, 126), -1)

    # Perform a simple non-max suppression
    rects, _ = cv2.groupRectangles(rects, 1, 1)

    return rects


def crop_board(screen: ndarray = cv2.imread('chessPiecesImg/Screenshot_1.png'),
               board: ndarray = cv2.imread('chessPiecesImg/screenshot_emptyboard.png')):
    board_coords = get_board_coords(screen, board)
    print(f"Board coords: {board_coords}")
    x0, x1, y0, y1 = board_coords[0], board_coords[0] + board_coords[2], board_coords[1], board_coords[1] + \
                                      board_coords[3]
    screen_cropped = (screen[y0: y1, x0: x1]).copy()

    return screen_cropped, board_coords


def get_board_coords(screen: ndarray = cv2.imread('chessPiecesImg/Screenshot_1.png'),
                     board: ndarray = cv2.imread('chessPiecesImg/screenshot_emptyboard.png')):
    return find_template_multiple(screen, board, threshold=0.01)[0]


def check_color(board_img: ndarray, piece_img: ndarray, rect: List) -> bool:
    x0, x1, y0, y1 = rect[0], rect[0] + rect[2], rect[1], rect[1] + rect[3]
    # Dá crop na board apenas no lugar da peça
    crop = (board_img[y0: y1, x0: x1]).copy()

    diff = cv2.absdiff(piece_img, crop)
    avg_diff = cv2.mean(diff)[0] / 255
    return avg_diff < 0.3  # Baixo do limiar é peça preta


def match_colors(board: ndarray, piece_imgs: List[ndarray], rects: List) -> List:
    pairs = zip(piece_imgs, rects)
    return [[check_color(board, img, r) for r in rect] for img, rect in pairs]


def match_color_rect(rects: List, colors: List) -> List:
    return [[r for (r, is_matching) in zip(rect, color) if is_matching] for rect, color in zip(rects, colors)]


def draw_results(img, rects, i):
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
    print(f"{i}: {rects}")
    for r in rects:
        cv2.rectangle(img, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (0, 0, 255), 2)
        if i != 12:
            print(f"     {n_to_name[i]}")
            print()
            cv2.putText(
                img, n_to_name[i], (r[0] + 5, r[1] + 25), cv2.FONT_HERSHEY_DUPLEX, 0.9, color=(0, 0, 255), thickness=2)


def draw_results_squares(board_img: ndarray, rects: List):
    for i, rect in enumerate(rects):
        draw_results(board_img, rect, i)


def detect_pieces(screenshot: ndarray, piece_imgs: List[ndarray]):
    screenshot_gray = grayscale_img(screenshot)
    screenshot_grad = morph_grad_img(screenshot_gray)

    piece_imgs_gray = [grayscale_img(img) for img in piece_imgs]
    piece_imgs_grad = [morph_grad_img(img) for img in piece_imgs_gray]

    cv2.imshow('screen', screenshot_gray)
    cv2.imshow('board', piece_imgs_gray[-1])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imshow('screen', screenshot_grad)
    cv2.imshow('board', piece_imgs_grad[-1])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    board_img, corners = crop_board(screenshot_grad, piece_imgs_grad[-1])
    add_board = np.hstack((corners[:2], [0, 0]))
    rects = [find_template_multiple(board_img, img) for img in piece_imgs_grad]
    """ Adicionar a posição da board na screenshot original para os quadrados ficarem alinhados"""
    rects = [[r + add_board for r in rect] for rect in rects]
    rects[-1] = [corners]

    colors_list = match_colors(screenshot_gray, piece_imgs_gray, rects)
    matching_color_rects = match_color_rect(rects, colors_list)
    draw_results_squares(screenshot, matching_color_rects)
    return matching_color_rects


def determine_pieces_squares(rects):
    # dict = {id_piece : (0,0)} # peça com id x, está na posição (0,0) que é top right
    rects_copy = rects.copy()
    board_rect = rects_copy.pop(12)[0]
    tl_board = board_rect[:2]
    gap = abs(board_rect[0] - (board_rect[0] + board_rect[2])) / 8
    board_array = [[None for _ in range(8)] for _ in range(8)]
    for i, pieces in rects_copy.items():
        for piece in pieces:
            piece_x1 = piece[0]
            piece_x2 = piece[0] + piece[2]
            piece_y1 = piece[1]
            piece_y2 = piece[1] + piece[3]
            piece_center = (int((piece_x1 + piece_x2) / 2),
                            int((piece_y1 + piece_y2) / 2))
            piece_coord = np.floor((piece_center - tl_board) / gap)
            board_array[int(piece_coord[0])][int(piece_coord[1])] = i

    return np.fliplr(list(zip(*board_array[::-1])))


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


def resize_img(img: ndarray, scale=0.4) -> ndarray:
    dim = (int(img.shape[1] * scale), int(img.shape[0] * scale))
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


if __name__ == "__main__":
    # Load the chessEngine board and chessEngine piece images
    screenshot_image = cv2.imread('chessPiecesImg/Screenshot_1.png')
    screenshot_image2 = cv2.imread('chessPiecesImg/Screenshot_2.png')
    # screenshot_image3 = cv2.imread('chessPiecesImg/Screenshot_3.png') # Não precisa de resize
    piece_images = [
        cv2.imread('chessPiecesImg/white_pawn.png'),
        cv2.imread('chessPiecesImg/white_rook.png'),
        cv2.imread('chessPiecesImg/white_bishop.png'),
        cv2.imread('chessPiecesImg/white_knight.png'),
        cv2.imread('chessPiecesImg/white_king.png'),
        cv2.imread('chessPiecesImg/white_queen.png'),
        cv2.imread('chessPiecesImg/black_pawn.png'),
        cv2.imread('chessPiecesImg/black_rook.png'),
        cv2.imread('chessPiecesImg/black_bishop.png'),
        cv2.imread('chessPiecesImg/black_knight.png'),
        cv2.imread('chessPiecesImg/black_king.png'),
        cv2.imread('chessPiecesImg/black_queen.png'),
        cv2.imread('chessPiecesImg/screenshot_emptyboard.png')
    ]

    screenshot_image = resize_img(screenshot_image)
    piece_images = [resize_img(img) for img in piece_images]

    rectangles = detect_pieces(screenshot_image, piece_images)
    cv2.imshow('Result', screenshot_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # piece_coordinate_dict = determine_pieces_squares(rectangles)
    # FEN = fen_string(piece_coordinate_dict)
