from chess.adb.daoADB import DaoADB
from chess.util.move import Move


class MobileChess:
    def __init__(self, dao_adb: DaoADB) -> None:
        self.__dao_adb: DaoADB = dao_adb

    def is_white(self) -> bool:
        pass

    def play(self, move: Move) -> None:
        pass

    def has_adv_played(self) -> None:
        pass

    def get_adv_move(self) -> None:
        pass
