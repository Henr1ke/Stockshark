import time
from typing import Optional

from chess.adb.coordinates.coordinates import Coordinates
from chess.adb.coordinates.coordinates_pixel_4 import CoordinatesPixel4
from chess.adb.dao_adb import DaoADB


class MenuNavigator:
    WAIT_TIME = 2

    def __init__(self, dao_adb: DaoADB, coordinates: Coordinates) -> None:
        self.__dao_adb: DaoADB = dao_adb
        self.__coordinates: Coordinates = coordinates
        self.__tap_wait_time = MenuNavigator.WAIT_TIME

    def open_app(self, wait_time: float = 5) -> None:
        # para encontrar o nome do package da app pretendida instalei na Play Store
        # uma app chamada "Package Name Viewer 2.0"
        # encontrar a app (com.chessEngine é o nome do Android package):
        # adb shell dumpsys package | findstr Activity | findstr com.chessEngine

        # open app in package @app_path
        # self.__dao_adb.open_app("com.chess/.home.HomeActivity")
        self.__dao_adb.open_app("com.chess/.splash.SplashActivity")
        time.sleep(wait_time)

    def vs_friend(self, name: str, on_white_side: Optional[bool] = None, duration: Optional[int] = None,
                  wait_time: float = 2) -> None:
        self.__tap_wait_time = wait_time
        if duration is not None:
            assert duration in [1, 3, 5, 10, 30], "O tempo de jogo tem de ser 1, 3, 5, 10 ou 30 minutos"

        self.__tap_screen(*self.__coordinates.init_screen_play_coords())  # play
        self.__tap_screen(*self.__coordinates.vs_friend_coords())  # vs friend
        self.__tap_screen(*self.__coordinates.search_box_coords())  # search box
        self.__dao_adb.input_text(name)  # write friend name
        self.__tap_screen(*self.__coordinates.friend_coords())  # friend
        if duration is not None:
            self.__tap_screen(*self.__coordinates.time_box_coords())  # time box
            self.__tap_screen(*self.__coordinates.time_coords(duration))
        self.__tap_screen(*self.__coordinates.player_color_coords(on_white_side))  # choose color
        self.__tap_screen(*self.__coordinates.bottom_green_btn_coords())  # play

    def vs_computer(self, diff_lvl: int, on_white_side: Optional[bool] = None, wait_time: float = 2) -> None:
        self.__tap_wait_time = wait_time
        accepted_diff_lvls = [1, 2, 3, 4, 5]
        assert diff_lvl in accepted_diff_lvls, "O nivel de dificuldade não está disponível"

        self.__tap_screen(*self.__coordinates.init_screen_play_coords())  # play
        self.__tap_screen(*self.__coordinates.vs_computer_coords())  # vs computer
        self.__tap_screen(*self.__coordinates.computer_coords(diff_lvl))
        self.__tap_screen(*self.__coordinates.bottom_green_btn_coords())  # confirm choosing
        self.__tap_screen(*self.__coordinates.computer_color_coords(on_white_side))  # choose color
        self.__tap_screen(*self.__coordinates.bottom_green_btn_coords())

    def __tap_screen(self, x: int, y: int) -> None:
        self.__dao_adb.tap_screen(x, y)
        time.sleep(self.__tap_wait_time)


if __name__ == '__main__':
    d = DaoADB()
    d.connect()
    c = CoordinatesPixel4()
    m = MenuNavigator(d, c)
    print("Oppening")
    m.open_app()
    print("Done")
    m.vs_computer(1)
