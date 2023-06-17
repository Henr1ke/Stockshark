from typing import Tuple, Optional

from stockshark.adb.coordinates.coordinates import Coordinates


class CoordinatesPixel4(Coordinates):

    def init_screen_play_coords(self) -> Tuple[int, int]:
        return 540, 1900

    def bottom_green_btn_coords(self) -> Tuple[int, int]:
        return 540, 2030

    def vs_friend_coords(self) -> Tuple[int, int]:
        return 540, 1170

    def search_box_coords(self) -> Tuple[int, int]:
        return 540, 330

    def friend_coords(self) -> Tuple[int, int]:
        return 540, 730

    def time_box_coords(self) -> Tuple[int, int]:
        return 540, 350

    def time_coords(self, time: int) -> Tuple[int, int]:
        if time == 1:
            return 200, 450
        if time == 3:
            return 200, 760
        if time == 5:
            return 880, 760
        if time == 10:
            return 200, 1240
        if time == 30:
            return 880, 1240

    def player_color_coords(self, is_white: Optional[bool]) -> Tuple[int, int]:
        if is_white is None:
            return 770, 1200
        return (580, 1200) if is_white else (950, 1200)

    def vs_computer_coords(self) -> Tuple[int, int]:
        return 540, 1360

    def computer_coords(self, diff_lvl: int) -> Tuple[int, int]:
        if diff_lvl == 1:
            return 165, 1030
        if diff_lvl == 2:
            return 355, 1030
        if diff_lvl == 3:
            return 540, 1030
        if diff_lvl == 4:
            return 725, 1030
        if diff_lvl == 5:
            return 915, 1030

    def computer_color_coords(self, is_white: Optional[bool]) -> Tuple[int, int]:
        if is_white is None:
            return 540, 815
        return (355, 815) if is_white else (725, 815)