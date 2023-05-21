from typing import Tuple, Optional

from chess.adb.coordinates.coordinates import Coordinates


class CoordinatesMi8Lite(Coordinates):

    def init_screen_play_coords(self) -> Tuple[int, int]:
        return 540, 1900

    def bottom_green_btn_coords(self) -> Tuple[int, int]:
        return 540, 2050

    def vs_friend_coords(self) -> Tuple[int, int]:
        return 540, 1180

    def search_box_coords(self) -> Tuple[int, int]:
        return 540, 350

    def friend_coords(self) -> Tuple[int, int]:
        return 540, 750

    def time_box_coords(self) -> Tuple[int, int]:
        return 540, 350

    def time_coords(self, time: int) -> Tuple[int, int]:
        if time == 1:
            return 200, 450
        if time == 3:
            return 200, 770
        if time == 5:
            return 900, 770
        if time == 10:
            return 200, 1070
        if time == 30:
            return 900, 1070

    def player_color_coords(self, is_white: Optional[bool]) -> Tuple[int, int]:
        if is_white is None:
            return 770, 1200
        return (580, 1200) if is_white else (950, 1200)

    def vs_computer_coords(self) -> Tuple[int, int]:
        return 540, 1370

    def computer_coords(self, diff_lvl: int) -> Tuple[int, int]:
        if diff_lvl == 1:
            return 170, 1000
        if diff_lvl == 2:
            return 350, 1000
        if diff_lvl == 3:
            return 540, 1000
        if diff_lvl == 4:
            return 725, 1000
        if diff_lvl == 5:
            return 910, 1000

    def computer_color_coords(self, is_white: Optional[bool]) -> Tuple[int, int]:
        if is_white is None:
            return 540, 850
        return (355, 850) if is_white else (725, 850)

    def board_tl_corner_coords_player(self) -> Tuple[int, int]:
        return 0, 615

    def board_tl_corner_coords_computer(self) -> Tuple[int, int]:
        return 0, 625

    def board_width(self) -> int:
        return 1080
