from __future__ import annotations

from copy import copy
from typing import Dict, Optional, List

from chess.piece.constants import CHAR_TO_PIECE_CLASS
from chess.piece.pawn import Pawn
from chess.piece.piece import Piece
from chess.piece.king import King
from chess.sim.visualizer import Visualizer
from chess.util.chessException import ChessException
from chess.util.move import Move
from chess.util.position import Position


class Board:
    def __init__(self, fen_str: str = "8/8/8/8/8/8/8/8") -> None:

        self.__tiles: List[List[Optional[Piece]]] = [[None] * 8 for _ in range(8)]
        self.__pieces_pos: Dict[Piece, Position] = dict()
        self.__kings_pos: Dict[bool, Position] = dict()

        for row, fen_substr in enumerate(fen_str.split("/")[::-1]):
            col = 0
            for char in fen_substr:
                if char.isdigit():
                    col += int(char)

                else:
                    piece_class = CHAR_TO_PIECE_CLASS[char.lower()]
                    is_white = char.isupper()
                    piece = piece_class(is_white)

                    self.add_piece(piece, col, row)
                    col += 1

    def __getitem__(self, *pos_args) -> Optional[Piece]:
        if isinstance(pos_args[0], tuple):
            pos_args = pos_args[0]
        pos = Position(*pos_args)
        return self.__tiles[8 - 1 - pos.row][pos.col]

    def __copy__(self) -> Board:
        cls = self.__class__
        board = cls.__new__(cls)
        for key, value in self.__dict__.items():
            if key == "_Board__tiles":
                tiles = [[piece for piece in row] for row in value]
                setattr(board, key, tiles)
            else:
                setattr(board, key, copy(value))
        return board

    def add_piece(self, piece: Piece, *pos_args) -> None:
        if not isinstance(piece, Piece):
            raise ChessException(f"Must add a Piece object to the board, got {piece} of type {type(piece)}")
        if isinstance(piece, King) and piece.is_white in self.__kings_pos.keys():
            raise ChessException(f"The board already contains a king of that color, it is not allowed to add another")

        pos = Position(*pos_args)
        if self[pos] is not None:
            self.clear_pos(pos)

        if isinstance(piece, King):
            self.__kings_pos[piece.is_white] = pos
        self.__pieces_pos[piece] = pos

        self.__tiles[8 - 1 - pos.row][pos.col] = piece

    def make_move(self, move: Move) -> Piece:
        piece = self[move.start_pos]
        if not isinstance(piece, Piece):
            raise ChessException("There is no piece on the move starting position")

        if self[move.end_pos] is not None:
            self.clear_pos(move.end_pos)

        if isinstance(piece, King):
            self.__kings_pos[piece.is_white] = move.end_pos
        self.__pieces_pos[piece] = move.end_pos

        self.__tiles[8 - 1 - move.start_pos.row][move.start_pos.col] = None
        self.__tiles[8 - 1 - move.end_pos.row][move.end_pos.col] = piece

        return piece

    def clear_pos(self, *pos_args) -> None:
        pos = Position(*pos_args)
        piece = self.__tiles[8 - 1 - pos.row][pos.col]

        if piece is not None:
            self.__pieces_pos.pop(piece, None)
            if isinstance(piece, King):
                self.__kings_pos.pop(piece.is_white, None)
            self.__tiles[8 - 1 - pos.row][pos.col] = None

        return piece

    @property
    def pieces_pos(self) -> Dict[Piece, Position]:
        return copy(self.__pieces_pos)

    @property
    def kings_pos(self) -> Dict[bool, Position]:
        return copy(self.__kings_pos)

    def gen_fen_str(self) -> str:
        piece_class_to_char = {val: key for (key, val) in CHAR_TO_PIECE_CLASS.items()}

        fen_substrs = []

        for i, row in enumerate(self.__tiles):
            fen_substr = ""
            tile_skips = 0
            for piece in row:
                if piece is None:
                    tile_skips += 1
                else:
                    if tile_skips > 0:
                        fen_substr += str(tile_skips)
                        tile_skips = 0
                    letter = piece_class_to_char[type(piece)]
                    fen_substr += letter.upper() if piece.is_white else letter.lower()

            if tile_skips > 0:
                fen_substr += str(tile_skips)
            fen_substrs.append(fen_substr)

        return "/".join(fen_substrs)


if __name__ == '__main__':
    v = Visualizer(Visualizer.PIECE_TO_LETTER)
    b = Board()

    b.add_piece(Pawn(True), "b3")
    b.add_piece(King(False), 0, 0)
    b.add_piece(Pawn(False), Position(4, 7))
    v.print_board(b)
    print()

    print(b["b3"])
    print(b[0, 0])
    print(b[Position(4, 7)])
    print()

    bc = copy(b)
    print(b["b3"] == bc["b3"])
    print()

    sp = Position("b3")
    ep = sp + (2, 0)
    bc.make_move(Move(sp, ep))
    v.print_board(b)
    v.print_board(bc)
    print({key: str(value) for key, value in b.kings_pos.items()})
    print({key: str(value) for key, value in bc.pieces_pos.items()})
    print()

    print(b.gen_fen_str())
    print()

    b.clear_pos("b3")
    b.clear_pos(0, 0)
    b.clear_pos(Position(4, 7))
    v.print_board(b)
    print()