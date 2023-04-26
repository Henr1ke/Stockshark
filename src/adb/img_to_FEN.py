import cv2
import numpy as np


def convert_to_gray(pieces):
    gray_pieces = {}
    for id, img in pieces.items():
        gray_pieces[id] = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_pieces


def morph_gray_grad(pieces, kernel):
    grad_pieces = {}
    for id, img in pieces.items():
        grad_pieces[id] = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
    return grad_pieces


def find_template_multiple(board, piece):
    # Este método apenas dá atenção ao formato da peça, não interessa a cor
    rects = []
    w, h = piece.shape[1], piece.shape[0]
    # cv2.imshow('Result', piece)
    # cv2.imshow('Result1', board)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    res = cv2.matchTemplate(board, piece, cv2.TM_CCOEFF_NORMED)
    threshold = 0.53  # matching threshold, relatively stable.
    loc = np.where(res >= threshold)

    for pt in zip(*loc[::-1]):
        rects.append((pt[0], pt[1], w, h))

    # Perform a simple non-max suppression
    rects, _ = cv2.groupRectangles(rects, 1, 1)

    # Flatten list of list to list of elements
    rects = [r for r in rects]

    return rects


def get_board_coords(screen=cv2.imread('Screenshot_1.png'), board=cv2.imread('../screenshot_emptyboard.png')):
    try:
        return find_template_multiple(screen, board)[0]
    except:
        return []


def find_multiple_temp_multiple(board, pieces):
    rects = {}
    for id, img in pieces.items():
        rects[id] = find_template_multiple(board, img)
    return rects


def check_color(board_img, piece_img, rect):
    y0, y1, x0, x1 = rect[1], rect[1] + rect[3], rect[0], rect[0] + rect[2]
    # Dá crop na board apenas no lugar da peça
    crop = (board_img[y0: y1, x0: x1]).copy()
    diff = cv2.absdiff(piece_img, crop)
    avg_diff = cv2.mean(diff)[0] / 255
    return avg_diff < 0.3  # Baixo do limiar é peça preta


def match_colors(board, pieces, rects):
    color_list = {}  # {id_piece: [True|False] # [White|Black]
    for id, img in pieces.items():
        rect_list = []
        for r in rects[id]:
            rect_list.append(check_color(board, img, r))
        color_list[id] = rect_list
    return color_list


def match_color_rect(rects, colors):
    cr_list = {}
    for id in rects:
        cr_list[id] = [r for (r, is_matching) in zip(
            rects[id], colors[id]) if is_matching]
    return cr_list


def draw_results(img, rects, id):
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
    for r in rects:
        # print(r)
        cv2.rectangle(img, (r[0], r[1]), (r[0] + r[2],
                                          r[1] + r[3]), (0, 0, 255), 2)
        if id != 13:
            cv2.putText(img, n_to_name[id], (r[0] + 5, r[1] + 25),
                        cv2.FONT_HERSHEY_DUPLEX, 0.9, color=(0, 0, 255), thickness=2)


def draw_results_squares(board_img, rects):
    for id, r in rects.items():
        draw_results(board_img, r, id)


def detect_pieces(screen, pieces):
    pieces_gray = convert_to_gray(pieces)
    s = 3
    kernel = np.ones((s, s), np.uint8)
    pieces_gray_grad = morph_gray_grad(pieces_gray, kernel)
    only_pieces = {k: pieces_gray_grad[k]
                   for k in pieces_gray_grad.keys() - {0}}
    rectangles = find_multiple_temp_multiple(pieces_gray_grad[0], only_pieces)
    only_pieces = {k: pieces_gray[k] for k in pieces_gray.keys() - {0}}
    colors_list = match_colors(pieces_gray[0], only_pieces, rectangles)
    matching_color_rects = match_color_rect(rectangles, colors_list)
    draw_results_squares(screen, matching_color_rects)
    return matching_color_rects


def determine_pieces_squares(rects):
    # dict = {id_piece : (0,0)} # peça com id x, está na posição (0,0) que é top right
    rects_copy = rects.copy()
    board_rect = rects_copy.pop(13)[0]
    print(rects_copy)
    tl_board = board_rect[:2]
    gap = abs(board_rect[0] - (board_rect[0] + board_rect[2])) / 8
    board_array = [[None for _ in range(8)] for _ in range(8)]
    for id, pieces in rects_copy.items():
        for piece in pieces:
            pieceX1 = piece[0]
            pieceX2 = piece[0] + piece[2]
            pieceY1 = piece[1]
            pieceY2 = piece[1] + piece[3]
            piece_center = (int((pieceX1 + pieceX2) / 2),
                            int((pieceY1 + pieceY2) / 2))
            piece_coord = np.floor((piece_center - tl_board) / gap)
            board_array[int(piece_coord[0])][int(piece_coord[1])] = id

    return np.fliplr(list(zip(*board_array[::-1])))


def FEN_string(board_array):
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


def resize_imgs(pieces, scale_percent):
    resized_pieces = {}
    for id, img in pieces.items():
        w = int(img.shape[1] * scale_percent / 100)
        h = int(img.shape[0] * scale_percent / 100)
        dim = (w, h)

        resized_pieces[id] = cv2.resize(
            img, dim, interpolation=cv2.INTER_AREA)
    return resized_pieces


if __name__ == "__main__":
    # Load the chessEngine board and chessEngine piece images
    screenshot = cv2.imread('../chessPiecesImg/Screenshot_1.png')
    white_pawn = cv2.imread('../chessPiecesImg/white_pawn.png')
    white_rook = cv2.imread('../chessPiecesImg/white_rook.png')
    white_bishop = cv2.imread('../chessPiecesImg/white_bishop.png')
    white_knight = cv2.imread('../chessPiecesImg/white_knight.png')
    white_king = cv2.imread('../chessPiecesImg/white_king.png')
    white_queen = cv2.imread('../chessPiecesImg/white_queen.png')
    black_pawn = cv2.imread('../chessPiecesImg/black_pawn.png')
    black_rook = cv2.imread('../chessPiecesImg/black_rook.png')
    black_bishop = cv2.imread('../chessPiecesImg/black_bishop.png')
    black_knight = cv2.imread('../chessPiecesImg/black_knight.png')
    black_king = cv2.imread('../chessPiecesImg/black_king.png')
    black_queen = cv2.imread('../chessPiecesImg/black_queen.png')
    img_board = cv2.imread('../chessPiecesImg/screenshot_emptyboard.png')

    pieces = {0: screenshot,
              1: white_pawn,
              2: white_rook,
              3: white_bishop,
              4: white_knight,
              5: white_king,
              6: white_queen,
              7: black_pawn,
              8: black_rook,
              9: black_bishop,
              10: black_knight,
              11: black_king,
              12: black_queen,
              13: img_board}

    scale = 40
    pieces = resize_imgs(pieces, scale)
    rectangles = detect_pieces(pieces[0], pieces)
    cv2.imshow('Result', pieces[0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    piece_coordinate_dict = determine_pieces_squares(rectangles)
    FEN = FEN_string(piece_coordinate_dict)
    print(FEN)
