from chess.adb.daoADB import DaoADB
from chess.img_process.identifier import Identifier
from chess.util.move import Move


class MobileChess:
    def __init__(self, dao_adb: DaoADB) -> None:
        self.__dao_adb: DaoADB = dao_adb

    def is_white(self) -> bool:
        pass

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
