from __future__ import annotations

from copy import copy
from typing import List, Optional

from stockshark.chess_engine.board import Board
from stockshark.chess_engine.move_validator import MoveValidator
from stockshark.chess_engine_2.chess_engine import ChessEngine
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
        game = cls.__new__(cls)
        for key, value in self.__dict__.items():
            if key == "_Game__legal_piece_moves":
                legal_piece_moves = {piece: copy(moves) for piece, moves in self.__legal_piece_moves.items()}
                setattr(game, key, legal_piece_moves)
            else:
                setattr(game, key, copy(value))
        return game

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

        if move.end_tile == self.__en_passant_target:
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
                self.__castlings = self.__castlings.replace("Q" if row_idx == 0 else "q", "")
                self.__castlings = self.__castlings.replace("K" if row_idx == 0 else "k", "")

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
                self.__castlings = self.__castlings.replace("Q" if row_idx == 0 else "q", "")
                return
            elif move.start_tile == Tile(k_side_col_idx, row_idx) \
                    or move.end_tile == Tile(k_side_col_idx, row_idx):
                self.__castlings = self.__castlings.replace("K" if row_idx == 0 else "k", "")
                return

    def _make_move(self, move: str) -> None:
        move = Move(move)
        return self.make_move(move)

    def make_move(self, move: Move) -> None:
        move = Move(move)

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
        self.__en_passant_target = e_p_target

        # Update self.__is_white_turn
        self.__is_white_turn = not self.__is_white_turn

        # Update self.__halfclock
        self.__halfclock = 0 if should_reset_halfclock else self.__halfclock + 1

        # Update self.__fullclock
        if self.__is_white_turn:
            self.__fullclock += 1

    def _gen_available_moves(self) -> List[str]:
        return [move.to_uci() for move in self.gen_available_moves()]

    def gen_available_moves(self) -> List[Move]:
        moves = []

        pieces = self.__board.pieces_tiles.keys()
        for piece in pieces:
            if piece.is_white != self.__is_white_turn:
                continue

            pseudo_moves = piece.gen_moves(self.__board)

            moves += [move for move in pseudo_moves if not MoveValidator.leaves_king_under_atk(self, move)]

        return moves

    def _gen_fen(self) -> str:
        fen_str_fields = [
            self.__board.gen_fen_str(),
            "w" if self.__is_white_turn else "b",
            "-" if len(self.__castling_rights) == 0 else self.__castling_rights,
            "-" if self.__ep_target is None else str(self.__ep_target),
            str(self.__halfclock),
            str(self.__fullclock)
        ]

        return " ".join(fen_str_fields)


if __name__ == '__main__':
    game = StocksharkEngine()
    print(game.ep_target)
