from typing import Optional

from chess.adb.coordinates.coordinates import Coordinates
from chess.adb.coordinates.coordinatesPixel4 import CoordinatesPixel4
from chess.adb.daoADB import DaoADB


class MenuNavigator:

    def __init__(self, dao_adb: DaoADB, coordinates: Coordinates) -> None:
        self.__dao_adb: DaoADB = dao_adb
        self.__coordinates: Coordinates = coordinates

    def open_app(self) -> None:
        # para encontrar o nome do package da app pretendida instalei na Play Store
        # uma app chamada "Package Name Viewer 2.0"
        # encontrar a app (com.chessEngine é o nome do Android package):
        # adb shell dumpsys package | findstr Activity | findstr com.chessEngine

        # open app in package @app_path
        self.__dao_adb.open_app("com.chess/.home.HomeActivity")

    def vs_player(self, name: str, is_white: Optional[bool] = None, time_control: int = 10) -> None:
        assert time_control in [1, 3, 5, 10, 30], "O tempo de jogo tem de ser 1, 3, 5, 10 ou 30 minutos"

        def choose_time():
            self.__dao_adb.tap_screen(*self.__coordinates.time_box_coords())  # time box
            self.__dao_adb.tap_screen(*self.__coordinates.time_coords(time_control))
            # if time_control == 1:
            #     self.__dao_adb.tap_screen(*TIME1)
            # elif time_control == 3:
            #     self.__dao_adb.tap_screen(*TIME3)
            # elif time_control == 5:
            #     self.__dao_adb.tap_screen(*TIME5)
            # elif time_control == 10:
            #     self.__dao_adb.tap_screen(*TIME10)
            # elif time_control == 30:
            #     self.__dao_adb.tap_screen(*TIME30)

        self.__dao_adb.tap_screen(*self.__coordinates.init_screen_play_coords())  # play
        self.__dao_adb.tap_screen(*self.__coordinates.vs_friend_coords())  # vs friend
        self.__dao_adb.tap_screen(*self.__coordinates.search_box_coords())  # search box
        self.__dao_adb.input_text(name)  # write friend name
        self.__dao_adb.tap_screen(*self.__coordinates.friend_coords())  # friend
        choose_time()  # choose time control
        self.__dao_adb.tap_screen(*self.__coordinates.player_color_coords(is_white))  # choose color
        self.__dao_adb.tap_screen(*self.__coordinates.bottom_green_btn_coords())  # play

    def vs_bot(self, diff_lvl: int, is_white: Optional[bool] = None) -> None:
        # TODO Os bots vão mudar no final de maio, refazer isto depois
        def choose_bot():
            self.__dao_adb.tap_screen(*self.__coordinates.bot_coords(diff_lvl))
            # if diff_lvl == 1:
            #     self.__dao_adb.tap_screen(*BOT1)
            # elif diff_lvl == 2:
            #     self.__dao_adb.tap_screen(*BOT2)
            # elif diff_lvl == 3:
            #     self.__dao_adb.tap_screen(*BOT3)
            # elif diff_lvl == 4:
            #     self.__dao_adb.tap_screen(*BOT4)
            # elif diff_lvl == 5:
            #     self.__dao_adb.tap_screen(*BOT5)
            self.__dao_adb.tap_screen(*self.__coordinates.bottom_green_btn_coords())  # confirm choosing

        self.__dao_adb.tap_screen(*self.__coordinates.init_screen_play_coords())  # play
        self.__dao_adb.tap_screen(*self.__coordinates.vs_bot_coords())  # vs computer
        choose_bot()  # choose enemy bot and
        self.__dao_adb.tap_screen(*self.__coordinates.bot_color_coords(is_white))  # choose color
        self.__dao_adb.tap_screen(*self.__coordinates.bottom_green_btn_coords())


if __name__ == '__main__':
    d = DaoADB()
    d.connect()
    c = CoordinatesPixel4()
    m = MenuNavigator(d, c)
    # m.open_app()
    m.vs_bot(1)
