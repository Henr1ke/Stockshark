from typing import Optional, Tuple, List

import cv2
from numpy import ndarray

from chess.art_vis.image_processing import ImageProcessing
from chess.art_vis.visual_debug import VisualDebug
from chess.util.position import Position


class Detector:

    # --------- TODO ------------- fazer com q o detector não seja uma classe estática pq tem de guardar o is_white para poder sar as funções loc_to_pos e pos_to_loc
    # TODO meter aqui as funções importantes do indentifier

    @staticmethod
    def get_board(screenshot: ndarray) -> Optional[ndarray]:
        scn_gray = ImageProcessing.grayscale(screenshot)
        scn_w = screenshot.shape[1]

        empty_board = ImageProcessing.read_img("chess_components/empty_board.png")
        size = (scn_w, scn_w)
        eb_resized = cv2.resize(empty_board, size, interpolation=cv2.INTER_AREA)
        empty_board_gray = ImageProcessing.grayscale(eb_resized)

        positions = ImageProcessing.locate(scn_gray, empty_board_gray, margin=2)
        if len(positions) == 1:
            pos = positions[0]
            board = ImageProcessing.crop(screenshot, 0, int(pos[1] - scn_w / 2), scn_w, int(pos[1] + scn_w / 2))
            return board
        return None

    @staticmethod
    def loc_to_pos(loc: Tuple[int, int], board_w: int) -> Position:
        col = int(8 * loc[0] / board_w)
        row = 7 - int(8 * loc[1] / board_w)
        return Position(col, row)

    @staticmethod
    def pos_to_loc(pos: Position, board_w: int) -> Tuple[int, int]:
        x = int(board_w / 2 + pos.col * board_w / 8)
        y = int(board_w / 2 + (7 - pos.row) * board_w / 8)
        return x, y

    @staticmethod
    def __get_piece_positions(board: ndarray, piece_name: str) -> List[Position]:
        board_gray = ImageProcessing.grayscale(board)
        board_w = board.shape[1]

        piece = ImageProcessing.read_img(f"chess_components/m_{piece_name}.png")
        size = (int(board_w / 8), int(board_w / 8))
        piece_resized = cv2.resize(piece, size, interpolation=cv2.INTER_AREA)
        piece_gray = ImageProcessing.grayscale(piece_resized)

        locations = ImageProcessing.locate(board_gray, piece_gray, margin=12)
        positions = [Detector.loc_to_pos(loc, board_w) for loc in locations]
        return positions

    @staticmethod
    def get_pawns_positions(board: ndarray) -> List[Position]:
        return Detector.__get_piece_positions(board, "pawn")

    @staticmethod
    def get_knights_positions(board: ndarray) -> List[Position]:
        return Detector.__get_piece_positions(board, "knight")

    @staticmethod
    def get_bishops_positions(board: ndarray) -> List[Position]:
        return Detector.__get_piece_positions(board, "bishop")

    @staticmethod
    def get_rooks_positions(board: ndarray) -> List[Position]:
        return Detector.__get_piece_positions(board, "rook")

    @staticmethod
    def get_queens_positions(board: ndarray) -> List[Position]:
        return Detector.__get_piece_positions(board, "queen")

    @staticmethod
    def get_kings_positions(board: ndarray) -> List[Position]:
        return Detector.__get_piece_positions(board, "king")


if __name__ == '__main__':
    scrn_img = ImageProcessing.read_img("screenshots/Screenshot.png")
    b_img = Detector.get_board(scrn_img)
    positions = Detector.get_pawns_positions(b_img)
    for pos in positions:
        print(pos.coord)
