from abc import ABC, abstractmethod
from typing import Tuple, Optional

from chess.util.position import Position


class Coordinates(ABC):

    @abstractmethod
    def init_screen_play_coords(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def bottom_green_btn_coords(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def vs_friend_coords(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def search_box_coords(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def friend_coords(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def time_box_coords(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def time_coords(self, time: int) -> Tuple[int, int]:
        pass

    @abstractmethod
    def player_color_coords(self, is_white: Optional[bool]) -> Tuple[int, int]:
        pass

    @abstractmethod
    def vs_computer_coords(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def computer_coords(self, diff_lvl: int) -> Tuple[int, int]:
        pass

    @abstractmethod
    def computer_color_coords(self, is_white: Optional[bool]) -> Tuple[int, int]:
        pass

    @abstractmethod
    def board_tl_corner_coords_player(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def board_tl_corner_coords_computer(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def board_width(self) -> int:
        pass

    def pos_coords(self, pos: Position, is_white: bool, tl_corner: Tuple[int, int]) -> Tuple[int, int]:
        tile_size = self.board_width() / 8
        if not is_white:
            pos = -pos

        x = int(tl_corner[0] + tile_size / 2 + tile_size * pos.col)
        y = int(tl_corner[1] + tile_size / 2 + tile_size * (7 - pos.row))
        return x, y
