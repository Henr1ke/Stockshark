from abc import ABC, abstractmethod
from typing import Tuple, Optional


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
