from __future__ import annotations
from typing import Tuple
from chess.util.constants import FILE_LETTERS

from chess.util.chess_exception import ChessException


class Position:
    """
    Position representation
            - by a pair of integeres:                                   - by a string coordinate:
               ╔════╦════╦════╦════╦════╦════╦════╦════╗                  ╔════╦════╦════╦════╦════╦════╦════╦════╗
               ║ 0,7║ 1,7║ 2,7║ 3,7║ 4,7║ 5,7║ 6,7║ 7,7║                  ║ a8 ║ b8 ║ c8 ║ d8 ║ e8 ║ f8 ║ g8 ║ h8 ║
               ╠════╬════╬════╬════╬════╬════╬════╬════╣                  ╠════╬════╬════╬════╬════╬════╬════╬════╣
               ║ 0,6║ 1,6║ 2,6║ 3,6║ 4,6║ 5,6║ 6,6║ 7,6║                  ║ a7 ║ b7 ║ c7 ║ d7 ║ e7 ║ f7 ║ g7 ║ h7 ║
               ╠════╬════╬════╬════╬════╬════╬════╬════╣                  ╠════╬════╬════╬════╬════╬════╬════╬════╣
               ║ 0,5║ 1,5║ 2,5║ 3,5║ 4,5║ 5,5║ 6,5║ 7,5║                  ║ a6 ║ b6 ║ c6 ║ d6 ║ e6 ║ f6 ║ g6 ║ h6 ║
               ╠════╬════╬════╬════╬════╬════╬════╬════╣                  ╠════╬════╬════╬════╬════╬════╬════╬════╣
               ║ 0,4║ 1,4║ 2,4║ 3,4║ 4,4║ 5,4║ 6,4║ 7,4║                  ║ a5 ║ b5 ║ c5 ║ d5 ║ e5 ║ f5 ║ g5 ║ h5 ║
               ╠════╬════╬════╬════╬════╬════╬════╬════╣                  ╠════╬════╬════╬════╬════╬════╬════╬════╣
               ║ 0,3║ 1,3║ 2,3║ 3,3║ 4,3║ 5,3║ 6,3║ 7,3║                  ║ a4 ║ b4 ║ c4 ║ d4 ║ e4 ║ f4 ║ g4 ║ h4 ║
           ^   ╠════╬════╬════╬════╬════╬════╬════╬════╣                  ╠════╬════╬════╬════╬════╬════╬════╬════╣
           |   ║ 0,2║ 1,2║ 2,2║ 3,2║ 4,2║ 5,2║ 6,2║ 7,2║            ^     ║ a3 ║ b3 ║ c3 ║ d3 ║ e3 ║ f3 ║ g3 ║ h3 ║
           |   ╠════╬════╬════╬════╬════╬════╬════╬════╣            |     ╠════╬════╬════╬════╬════╬════╬════╬════╣
           |   ║ 0,1║ 1,1║ 2,1║ 3,1║ 4,1║ 5,1║ 6,1║ 7,1║            |     ║ a2 ║ b2 ║ c2 ║ d2 ║ e2 ║ f2 ║ g2 ║ h2 ║
         Rows  ╠════╬════╬════╬════╬════╬════╬════╬════╣            |     ╠════╬════╬════╬════╬════╬════╬════╬════╣
       (Second ║ 0,0║ 1,0║ 2,0║ 3,0║ 4,0║ 5,0║ 6,0║ 7,0║          Ranks   ║ a1 ║ b1 ║ c1 ║ d1 ║ e1 ║ f1 ║ g1 ║ h1 ║
        Index) ╚════╩════╩════╩════╩════╩════╩════╩════╝        (Numbers) ╚════╩════╩════╩════╩════╩════╩════╩════╝
                Columns (First index) --->                                Files (Letters) --->
    """

    def __init__(self, *args) -> None:
        if len(args) == 1 and type(args[0]) == Position:
            self._init_with_pos(args[0])

        elif len(args) == 1 and type(args[0]) == str:
            self._init_with_coord(args[0])

        elif len(args) == 2 and type(args[0]) == int and type(args[1]) == int:
            self._init_with_col_row(args[0], args[1])

        else:
            raise ValueError(
                f"Cannot initialize a Position with parameter types {[type(parameter) for parameter in args]}")

    def __hash__(self) -> int:
        number = 8 * self.row + self.col
        return hash(number)

    def __eq__(self, pos: Position) -> bool:
        return isinstance(pos, Position) and self.__row == pos.__row and self.__col == pos.__col

    def __lt__(self, pos: Position) -> bool:
        if not isinstance(pos, Position):
            return False

        if self.row != pos.row:
            return self.row < pos.row
        return self.col < pos.col

    def __gt__(self, pos: Position) -> bool:
        return pos < self

    def __add__(self, inc: Tuple[int, int]) -> Position:
        if not (isinstance(inc, tuple) and len(inc) == 2 and
                isinstance(inc[0], int) and isinstance(inc[1], int)):
            raise ChessException(f"Expected a tuple containing 2 integers, got {inc} of type {type(inc)}")

        return Position(self.col + inc[0], self.row + inc[1])

    def __neg__(self):
        return Position(7 - self.col, 7 - self.row)

    def __repr__(self) -> str:
        return self.__coord

    @property
    def row(self) -> int:
        return self.__row

    @property
    def col(self) -> int:
        return self.__col

    @property
    def coord(self) -> str:
        return self.__coord

    def _init_with_col_row(self, col: int, row: int) -> None:
        if not (0 <= col < 8):
            raise ChessException(f"Column must be from 0 to 7, got {col}")
        if not (0 <= row < 8):
            raise ChessException(f"Row must be from 0 to 7, got {row}")

        self.__col: int = col
        self.__row: int = row
        self.__coord: str = FILE_LETTERS[col] + str(row + 1)

    def _init_with_coord(self, coord: str) -> None:
        if len(coord) != 2:
            raise ChessException("The coordinate introduced must contain exactly 2 characters")

        if coord[0].lower() not in FILE_LETTERS:
            raise ChessException(f"The file (first character) must be a letter from \"{FILE_LETTERS[0]}\" to "
                                 f"\"{FILE_LETTERS[-1]}\"")

        if not coord[1].isdigit() or not (0 < int(coord[1]) <= 8):
            raise ChessException(f"The rank (second character) must be a number from 1 to 8")

        self.__col = FILE_LETTERS.index(coord[0])
        self.__row = int(coord[1]) - 1
        self.__coord = coord

    def _init_with_pos(self, pos: Position) -> None:
        self.__col: int = pos.__col
        self.__row: int = pos.__row
        self.__coord: str = pos.__coord


if __name__ == '__main__':
    for arguments in [["g5"], [0, 0], [Position("a3")], [(5, 5)], [], [19.5, 4, -7], [0, 8], ["ola"]]:
        try:
            p = Position(*arguments)
            print(f"arguments = {arguments}, p = {p}")
        except ValueError as e:
            print(f"Error: {e}")
        except ChessException as e:
            print(f"Error: {e}")
