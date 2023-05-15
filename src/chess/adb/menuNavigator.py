from chess.adb.daoADB import DaoADB


class MenuNavigator:

    def __init__(self, dao_adb: DaoADB) -> None:
        self.__dao_adb: DaoADB = dao_adb

    def open_app(self) -> None:
        pass

    def vs_player(self, name: str) -> None:
        pass

    def vs_bot(self, diff: int) -> None:
        pass
