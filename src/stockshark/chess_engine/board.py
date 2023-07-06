from __future__ import annotations

from copy import copy
from typing import Dict, Optional, List, Type

from stockshark.piece.bishop import Bishop
from stockshark.piece.king import King
from stockshark.piece.knight import Knight
from stockshark.piece.pawn import Pawn
from stockshark.piece.piece import Piece
from stockshark.piece.queen import Queen
from stockshark.piece.rook import Rook
from stockshark.util.chess_exception import ChessException
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class Board:
    CHAR_TO_PIECE_CLASS: Dict[str, Type[Piece]] = {"p": Pawn, "n": Knight, "b": Bishop, "r": Rook, "q": Queen,
                                                   "k": King}

    def __init__(self, fen: str = "8/8/8/8/8/8/8/8") -> None:

        self.__tiles: List[List[Optional[Piece]]] = [[None] * 8 for _ in range(8)]
        self.__pieces_tiles: Dict[Piece, Tile] = dict()
        self.__kings: Dict[bool, King] = dict()

        for row, fen_substr in enumerate(fen.split("/")[::-1]):
            col = 0
            for char in fen_substr:
                if char.isdigit():
                    col += int(char)

                else:
                    piece_class = Board.CHAR_TO_PIECE_CLASS[char.lower()]
                    is_white = char.isupper()
                    piece = piece_class(is_white)

                    self.add_piece(piece, col, row)
                    col += 1

    def __getitem__(self, *tile_args) -> Optional[Piece]:
        if isinstance(tile_args[0], tuple):
            tile_args = tile_args[0]
        tile = Tile(*tile_args)
        return self.__tiles[7 - tile.row][tile.col]

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

    def make_move(self, move: Move) -> None:
        piece = self[move.start_tile]
        if piece is None:
            raise ChessException("There is no piece at the move starting tile")

        if self[move.end_tile] is not None:
            self.clear_tile(move.end_tile)

        self.__tiles[8 - 1 - move.start_tile.row][move.start_tile.col] = None
        self.__tiles[8 - 1 - move.end_tile.row][move.end_tile.col] = piece

        self.__pieces_tiles[piece] = move.end_tile

    def add_piece(self, piece: Piece, *tile_args) -> None:
        if not isinstance(piece, Piece):
            raise ChessException(f"Must add a Piece object to the board, got {piece} of type {type(piece)}")
        if isinstance(piece, King) and piece.is_white in self.__kings.keys():
            raise ChessException(f"The board already contains a king of that color, it is not allowed to add another")

        tile = Tile(*tile_args)
        if self[tile] is not None:
            self.clear_tile(tile)

        if isinstance(piece, King):
            self.__kings[piece.is_white] = piece
        self.__pieces_tiles[piece] = tile

        self.__tiles[8 - 1 - tile.row][tile.col] = piece

    def clear_tile(self, *tile_args) -> Optional[Piece]:
        tile = Tile(*tile_args)
        piece = self.__tiles[8 - 1 - tile.row][tile.col]

        if piece is not None:
            self.__pieces_tiles.pop(piece, None)
            if isinstance(piece, King):
                self.__kings.pop(piece.is_white, None)
            self.__tiles[8 - 1 - tile.row][tile.col] = None

        return piece

    @property
    def pieces_tiles(self) -> Dict[Piece, Tile]:
        return copy(self.__pieces_tiles)

    @property
    def kings(self) -> Dict[bool, King]:
        return copy(self.__kings)

    def gen_fen(self) -> str:
        piece_class_to_char = {piece_class: char for char, piece_class in Board.CHAR_TO_PIECE_CLASS.items()}

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
