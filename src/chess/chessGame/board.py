from __future__ import annotations

from copy import copy
from typing import Dict, Optional, List

from chess.piece.constants import CHAR_TO_PIECE_CLASS
from chess.piece.pawn import Pawn
from chess.piece.piece import Piece
from chess.piece.king import King
from chess.sim.visualizer import Visualizer
from chess.util.chess_exception import ChessException
from chess.util.move import Move
from chess.util.position import Position


class Board:
    def __init__(self, fen_str: str = "8/8/8/8/8/8/8/8") -> None:

        self.__tiles: List[List[Optional[Piece]]] = [[None] * 8 for _ in range(8)]
        self.__pieces_pos: Dict[Piece, Position] = dict()
        self.__kings: Dict[bool, King] = dict()

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
        return self.__tiles[7 - pos.row][pos.col]

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
        if isinstance(piece, King) and piece.is_white in self.__kings.keys():
            raise ChessException(f"The board already contains a king of that color, it is not allowed to add another")

        pos = Position(*pos_args)
        if self[pos] is not None:
            self.clear_pos(pos)

        if isinstance(piece, King):
            self.__kings[piece.is_white] = piece
        self.__pieces_pos[piece] = pos

        self.__tiles[8 - 1 - pos.row][pos.col] = piece

    def make_move(self, move: Move) -> None:
        if move.piece != self[move.start_pos]:
            raise ChessException("The moved piece does not exist or is not valid")

        if self[move.end_pos] is not None:
            self.clear_pos(move.end_pos)

        self.__tiles[8 - 1 - move.start_pos.row][move.start_pos.col] = None
        self.__tiles[8 - 1 - move.end_pos.row][move.end_pos.col] = move.piece

        self.__pieces_pos[move.piece] = move.end_pos

    def unmake_move(self, move: Move) -> None:
        if move.piece != self[move.end_pos]:
            raise ChessException("The moved piece does not exist or is not valid")

        self.__tiles[8 - 1 - move.start_pos.row][move.start_pos.col] = move.piece
        self.__tiles[8 - 1 - move.end_pos.row][move.end_pos.col] = None

        self.__pieces_pos[move.piece] = move.start_pos

        if move.eaten_piece is not None:
            self.add_piece(move.eaten_piece, move.end_pos)

        return move.piece

    def clear_pos(self, *pos_args) -> Optional[Piece]:
        pos = Position(*pos_args)
        piece = self.__tiles[8 - 1 - pos.row][pos.col]

        if piece is not None:
            self.__pieces_pos.pop(piece, None)
            if isinstance(piece, King):
                self.__kings.pop(piece.is_white, None)
            self.__tiles[8 - 1 - pos.row][pos.col] = None

        return piece

    @property
    def pieces_pos(self) -> Dict[Piece, Position]:
        return copy(self.__pieces_pos)

    @property
    def kings(self) -> Dict[bool, King]:
        return copy(self.__kings)

    def gen_fen_str(self) -> str:
        piece_class_to_char = {piece_class: char for char, piece_class in CHAR_TO_PIECE_CLASS.items()}

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
