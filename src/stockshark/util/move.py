from __future__ import annotations

from typing import Optional

from stockshark.util.chess_exception import ChessException
from stockshark.util.tile import Tile


class Move:
    PROMOTE_N = "n"
    PROMOTE_B = "b"
    PROMOTE_R = "r"
    PROMOTE_Q = "q"

    def __init__(self, start_tile_args, end_tile_args, promote_type: Optional[str] = None) -> None:
        start_tile = Tile(start_tile_args)
        end_tile = Tile(end_tile_args)

        if start_tile == end_tile:
            raise ChessException("A move cannot start and end on itself")

        if promote_type is not None and (promote_type not in [
            Move.PROMOTE_N,
            Move.PROMOTE_B,
            Move.PROMOTE_R,
            Move.PROMOTE_Q
        ] or not Move.__is_promotion_move_valid(start_tile, end_tile)):
            raise ChessException("Promotion move is not valid")

        self.__start_tile: Tile = start_tile
        self.__end_tile: Tile = end_tile
        self.__promote_type = promote_type

    def __hash__(self) -> int:
        return hash((self.__start_tile, self.__end_tile, self.__promote_type))

    def __eq__(self, other: Move) -> bool:
        return isinstance(other, Move) and self.start_tile == other.start_tile and self.end_tile == other.end_tile

    def __gt__(self, other: Move) -> bool:
        return False

    def __lt__(self, other: Move) -> bool:
        return False

    def __repr__(self) -> str:
        return self.to_uci()

    @staticmethod
    def from_uci(uci_str: str) -> Move:
        if len(uci_str) < 4 or len(uci_str) > 5:
            raise ChessException("UCI string must be 4 or 5 characters long")

        start_tile = Tile(uci_str[:2])
        end_tile = Tile(uci_str[2:4])
        promote_type = None if len(uci_str) == 4 else uci_str[4]

        return Move(start_tile, end_tile, promote_type)

    @staticmethod
    def __is_promotion_move_valid(start_tile: Tile, end_tile: Tile) -> bool:
        return start_tile.row == 6 and end_tile.row == 7 or start_tile.row == 1 and end_tile.row == 0

    @property
    def start_tile(self) -> Tile:
        return self.__start_tile

    @property
    def end_tile(self) -> Tile:
        return self.__end_tile

    @property
    def promote_type(self) -> Optional[str]:
        return self.__promote_type

    def to_uci(self):
        promote_piece_str = "" if self.__promote_type is None else self.__promote_type
        return f"{self.__start_tile}{self.__end_tile}{promote_piece_str}"
