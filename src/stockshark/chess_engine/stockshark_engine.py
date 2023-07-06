from __future__ import annotations

from copy import copy
from typing import Optional, Set

from stockshark.chess_engine.board import Board
from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.piece.bishop import Bishop
from stockshark.piece.king import King
from stockshark.piece.knight import Knight
from stockshark.piece.pawn import Pawn
from stockshark.piece.queen import Queen
from stockshark.piece.rook import Rook
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class StocksharkEngine(ChessEngine):

    def _new_game(self, fen: str):
        fen_fields = fen.split(" ")
        self.__board: Board = Board(fen_fields[0])
        self.__is_white_turn: bool = True if fen_fields[1] == "w" else False
        self.__castling_rights: str = fen_fields[2]
        self.__ep_target: Optional[Tile] = None if fen_fields[3] == "-" else Tile(fen_fields[3])
        self.__halfclock: int = int(fen_fields[4])
        self.__fullclock: int = int(fen_fields[5])

    def __copy__(self) -> StocksharkEngine:
        cls = self.__class__
        engine = cls.__new__(cls)
        for key, value in self.__dict__.items():
            setattr(engine, key, copy(value))
        return engine

    @property
    def board(self) -> Board:
        return copy(self.__board)

    @property
    def is_white_turn(self) -> bool:
        return self.__is_white_turn

    @property
    def castling_rights(self) -> str:
        return self.__castling_rights

    @property
    def ep_target(self) -> Optional[Tile]:
        return self.__ep_target

    @property
    def halfclock(self) -> int:
        return self.__halfclock

    @property
    def fullclock(self) -> int:
        return self.__fullclock

    def __pawn_actions(self, move: Move) -> Optional[Tile]:
        piece = self.__board[move.end_tile]

        if abs(move.start_tile.row - move.end_tile.row) == 2:
            return move.end_tile + ((0, -1) if piece.is_white else (0, 1))

        if move.end_tile == self.__ep_target:
            capt_piece_tile = move.end_tile + ((0, -1) if piece.is_white else (0, 1))
            self.__board.clear_tile(capt_piece_tile)
        elif move.promote_type is not None:
            promote_piece = None
            if move.promote_type == Move.PROMOTE_N:
                promote_piece = Knight(piece.is_white)
            elif move.promote_type == Move.PROMOTE_B:
                promote_piece = Bishop(piece.is_white)
            elif move.promote_type == Move.PROMOTE_R:
                promote_piece = Rook(piece.is_white)
            elif move.promote_type == Move.PROMOTE_Q:
                promote_piece = Queen(piece.is_white)

            if promote_piece is not None:
                self.__board.add_piece(promote_piece, move.end_tile)

    def __update_castlings(self, move: Move) -> None:
        king_col_idx = 4
        q_side_col_idx = 0
        k_side_col_idx = 7

        piece = self.__board[move.end_tile]

        for row_idx in (0, 7):
            if isinstance(piece, King) and move.start_tile == Tile(king_col_idx, row_idx):
                self.__castling_rights = self.__castling_rights.replace("Q" if row_idx == 0 else "q", "")
                self.__castling_rights = self.__castling_rights.replace("K" if row_idx == 0 else "k", "")

                if move.end_tile.col == 2:
                    start_tile = Tile(0, row_idx)
                    end_tile = move.end_tile + (1, 0)
                    self.__board.make_move(Move(start_tile, end_tile))
                elif move.end_tile.col == 6:
                    start_tile = Tile(7, row_idx)
                    end_tile = move.end_tile + (-1, 0)
                    self.__board.make_move(Move(start_tile, end_tile))

                return

            elif move.start_tile == Tile(q_side_col_idx, row_idx) \
                    or move.end_tile == Tile(q_side_col_idx, row_idx):
                self.__castling_rights = self.__castling_rights.replace("Q" if row_idx == 0 else "q", "")
                return
            elif move.start_tile == Tile(k_side_col_idx, row_idx) \
                    or move.end_tile == Tile(k_side_col_idx, row_idx):
                self.__castling_rights = self.__castling_rights.replace("K" if row_idx == 0 else "k", "")
                return

    def get_piece_at(self, tile: str) -> Optional[str]:
        try:
            tile = Tile(tile[0], tile[1])
            piece = self.__board[tile]
            return str(piece) if piece is not None else None
        except ValueError:
            return None

    def _make_move(self, move: str) -> None:
        move = Move.from_uci(move)
        self.make_move(move)

    def make_move(self, move: Move) -> None:
        piece = self.__board[move.start_tile]

        eaten_piece = self.__board[move.end_tile]

        should_reset_halfclock = eaten_piece is not None
        # Update self.__board
        self.__board.make_move(move)

        # Update self.__castlings
        self.__update_castlings(move)

        # Update self.__en_passants
        e_p_target = None
        if isinstance(piece, Pawn):
            should_reset_halfclock = True
            e_p_target = self.__pawn_actions(move)
        self.__ep_target = e_p_target

        # Update self.__is_white_turn
        self.__is_white_turn = not self.__is_white_turn

        # Update self.__halfclock
        self.__halfclock = 0 if should_reset_halfclock else self.__halfclock + 1

        # Update self.__fullclock
        if self.__is_white_turn:
            self.__fullclock += 1

    def _gen_attacked_tiles(self) -> Set[str]:
        attacked_tiles = set()

        pieces = self.__board.pieces_tiles.keys()
        for piece in pieces:
            if piece.is_white == self.__is_white_turn:
                continue

            attacked_tiles = attacked_tiles.union(piece.gen_attacked_tiles(self))

        return {tile.name for tile in attacked_tiles}

    def _gen_available_moves(self) -> Set[str]:
        moves = set()

        pieces = self.__board.pieces_tiles.keys()
        for piece in pieces:
            if piece.is_white != self.__is_white_turn:
                continue

            pseudo_moves = piece.gen_moves(self)

            moves = moves.union({move.to_uci() for move in pseudo_moves if not self.__leaves_king_under_atk(move)})

        return moves

    def _gen_fen(self) -> str:
        fen_fields = [
            self.__board.gen_fen(),
            "w" if self.__is_white_turn else "b",
            "-" if len(self.__castling_rights) == 0 else self.__castling_rights,
            "-" if self.__ep_target is None else str(self.__ep_target),
            str(self.__halfclock),
            str(self.__fullclock)
        ]

        return " ".join(fen_fields)

    def __king_is_under_atk(self) -> bool:
        is_king_white = not self.__is_white_turn
        if is_king_white not in self.__board.kings.keys():
            return False

        king = self.__board.kings[is_king_white]
        atk_pieces = [piece for piece in self.__board.pieces_tiles.keys() if piece.is_white is not is_king_white]

        for atk_piece in atk_pieces:
            moves = atk_piece.gen_moves(self)
            if king in [self.__board[move.end_tile] for move in moves]:
                return True
        return False

    def __leaves_king_under_atk(self, move: Move) -> bool:
        engine_copy = copy(self)
        engine_copy.make_move(move)
        return engine_copy.__king_is_under_atk()
