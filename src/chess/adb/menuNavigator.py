from typing import Optional

from chess.adb.daoADB import DaoADB
from adb.sim_adb.constants import *


class MenuNavigator:

    def __init__(self, dao_adb: DaoADB) -> None:
        self.__dao_adb: DaoADB = dao_adb

    def open_app(self) -> None:
        self.__dao_adb.open_app("com.chess/.home.HomeActivity")

    def vs_player(self, name: str, is_white: Optional[bool] = None, time_control: int = 10) -> None:
        assert time_control in [1, 3, 5, 10, 30], "O tempo de jogo tem de ser 1, 3, 5, 10 ou 30 minutos"

        def choose_time():
            self.__dao_adb.tap_screen(*TIMEBOX)  # time box
            if time_control == 1:
                self.__dao_adb.tap_screen(*TIME1)
            elif time_control == 3:
                self.__dao_adb.tap_screen(*TIME3)
            elif time_control == 5:
                self.__dao_adb.tap_screen(*TIME5)
            elif time_control == 10:
                self.__dao_adb.tap_screen(*TIME10)
            elif time_control == 30:
                self.__dao_adb.tap_screen(*TIME30)

        self.__dao_adb.tap_screen(*PLAY1)  # play
        self.__dao_adb.tap_screen(*VS_FRIEND)  # vs friend
        self.__dao_adb.tap_screen(*SEARCH_BOX)  # search box
        self.__dao_adb.input_text(name)  # write friend name
        self.__dao_adb.tap_screen(*FRIEND)  # friend
        choose_time()  # choose time control
        if is_white is not None:
            self.__dao_adb.tap_screen(*WHITE_PLAYER) if is_white else self.__dao_adb.tap_screen(
                *BLACK_PLAYER)  # choose color
        self.__dao_adb.tap_screen(*PLAY2)  # play

    def vs_bot(self, diff_lvl: int, is_white: Optional[bool] = None) -> None:
        # TODO Os bots vão mudar no final de maio, refazer isto depois
        def choose_bot():
            if diff_lvl == 1:
                self.__dao_adb.tap_screen(*BOT1)
            elif diff_lvl == 2:
                self.__dao_adb.tap_screen(*BOT2)
            elif diff_lvl == 3:
                self.__dao_adb.tap_screen(*BOT3)
            elif diff_lvl == 4:
                self.__dao_adb.tap_screen(*BOT4)
            elif diff_lvl == 5:
                self.__dao_adb.tap_screen(*BOT5)
            self.__dao_adb.tap_screen(*CONFIRM_BOT)  # confirm choosing

        self.__dao_adb.tap_screen(*PLAY1)  # play
        self.__dao_adb.tap_screen(*VS_BOT)  # vs computer
        choose_bot()  # choose enemy bot and
        if is_white is not None:
            self.__dao_adb.tap_screen(*WHITE_BOT) if is_white else self.__dao_adb.tap_screen(*BLACK_BOT)  # choose color
        self.__dao_adb.tap_screen(*PLAY3)
