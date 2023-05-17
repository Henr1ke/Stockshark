from chess.adb.daoADB import DaoADB
from chess.img_process.identifier import Identifier
from chess.util.move import Move


class MobileChess:
    def __init__(self, dao_adb: DaoADB) -> None:
        self.__dao_adb: DaoADB = dao_adb

    def is_white(self) -> bool:
        white_king = cv2.imread('../chessPiecesImg/white_king.png')
        black_king = cv2.imread('../chessPiecesImg/black_king.png')
        kings = white_king, black_king

        cropped_board = ProcessImage.crop()[0]
        board_gray = ProcessImage.grayscale(cropped_board)
        board_grad = ProcessImage.morph_grad(board_gray)

        kings_gray = [ProcessImage.grayscale(img) for img in kings]
        kings_grad = [ProcessImage.morph_grad(img) for img in kings_gray]

        kings_rects = [Identifier.find_template(board_grad, img) for img in kings_grad]
        kings_colors = Identifier.match_colors(board_gray, kings_gray, kings_rects)
        kings_color_rects = Identifier.match_color_rect(kings_rects, kings_colors)
        wk, bk = kings_color_rects[0][0], kings_color_rects[1][0]
        return wk[1] > bk[1]

    def play(self, move: Move) -> None:
        board_coords = Identifier.get_board_coords()
        botleft_corner = (board_coords[0], board_coords[1] + board_coords[3])
        gap = board_coords[2] / 8

        for pos in (move.start_pos, move.end_pos):
            x = int(botleft_corner[0] + gap * pos.col + gap / 2)
            y = int(botleft_corner[1] - gap * pos.row - gap / 2)
            self.__dao_adb.tap_screen(x, y)

    def has_adv_played(self) -> None:
        pass

    def get_adv_move(self) -> None:
        pass
