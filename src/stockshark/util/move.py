from __future__ import annotations

from stockshark.util.chess_exception import ChessException
from stockshark.util.tile import Tile


class Move:
    def __init__(self, start_tile_args, end_tile_args) -> None:
        start_tile = Tile(start_tile_args)
        end_tile = Tile(end_tile_args)

        if start_tile == end_tile:
            raise ChessException("A move cannot start and end on itself")

        self.__start_tile: Tile = start_tile
        self.__end_tile: Tile = end_tile

    def __eq__(self, other: Move) -> bool:
        return isinstance(other, Move) and self.start_tile == other.start_tile and self.end_tile == other.end_tile

    def __repr__(self) -> str:
        return f"{self.__start_tile}{self.__end_tile}"

    @property
    def start_tile(self) -> Tile:
        return self.__start_tile

    @property
    def end_tile(self) -> Tile:
        return self.__end_tile
