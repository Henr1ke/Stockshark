from __future__ import annotations

from copy import copy
from typing import Dict, Optional, List

from chess.piece.king import King
from chess.piece.pawn import Pawn
from chess.piece.piece import Piece
from chess.piece.queen import Queen
from chess.piece.rook import Rook
from chess.chessGame.board import Board
from chess.chessGame.chessRules import ChessRules
from chess.chessGame.state import State
from chess.util.move import Move
from chess.util.position import Position


class ChessGame:
    def __init__(self, fen_str: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
        fen_str_fields = fen_str.split()

        self.__board: Board = Board(fen_str_fields[0])
        self.__is_white_turn: bool = True if fen_str_fields[1] == "w" else False
        self.__castlings: str = fen_str_fields[2]
        self.__en_passant_target: Optional[Position] = None if fen_str_fields[3] == "-" else Position(fen_str_fields[3])
        self.__halfclock: int = int(fen_str_fields[4])
        self.__fullclock: int = int(fen_str_fields[5])
        self.__played_moves: List[Move] = []
        self.__state = State.IN_PROGRESS
        self.__legal_pieces_pos: Dict[Piece, List[Position]] = dict()

    def __copy__(self) -> ChessGame:
        cls = self.__class__
        game = cls.__new__(cls)
        for key, value in self.__dict__.items():
            if key == "_Game__legal_pieces_pos":
                legal_pieces_pos = {piece: copy(pos) for piece, pos in self.__legal_pieces_pos.items()}
                setattr(game, key, legal_pieces_pos)
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
    def castlings(self) -> str:
        return self.__castlings

    @property
    def en_passant_target(self) -> Optional[Position]:
        return self.__en_passant_target

    @property
    def halfclock(self) -> int:
        return self.__halfclock

    @property
    def fullclock(self) -> int:
        return self.__fullclock

    @property
    def played_moves(self) -> List[Move]:
        return copy(self.__played_moves)

    @property
    def state(self) -> State:
        return self.__state

    def gen_fen_str(self) -> str:
        fen_str_fields = [
            self.__board.gen_fen_str(),
            "w" if self.__is_white_turn else "b",
            "-" if len(self.__castlings) == 0 else self.__castlings,
            "-" if self.__en_passant_target is None else str(self.__en_passant_target),
            str(self.__halfclock),
            str(self.__fullclock)
        ]

        return " ".join(fen_str_fields)

    def get_legal_piece_pos(self, piece: Piece) -> List[Position]:
        if piece not in self.__legal_pieces_pos:
            positions = piece.gen_positions(self)

            # Only keeps the position if the move does not leave the king in check
            start_pos = piece.get_pos(self.board)
            legal_pos = [end_pos for end_pos in positions
                         if not ChessRules.leaves_king_under_atk(self, Move(start_pos, end_pos))]

            # Updates the dictionary
            self.__legal_pieces_pos[piece] = legal_pos

        return self.__legal_pieces_pos[piece]

    def play(self, move: Move, is_test=False) -> None:
        def pawn_actions(is_white: bool) -> Optional[Position]:
            if move.end_pos == self.__en_passant_target:
                capt_piece_pos = move.end_pos + ((0, -1) if is_white else (0, 1))
                self.__board.clear_pos(capt_piece_pos)
            elif move.end_pos.row == (7 if is_white else 0):
                self.__board.add_piece(Queen(is_white), move.end_pos)  # TODO its always promoting to queen

            if abs(move.start_pos.row - move.end_pos.row) == 2:
                return move.end_pos + ((0, -1) if is_white else (0, 1))

        def rook_actions(is_white: bool) -> None:
            initial_row = 0 if is_white else 7
            if move.start_pos.row == initial_row:
                if move.start_pos.col == 0:
                    self.__castlings = self.__castlings.replace("Q" if is_white else "q", "")
                elif move.start_pos.col == 7:
                    self.__castlings = self.__castlings.replace("K" if is_white else "k", "")

        def king_actions(is_white: bool) -> None:
            if move.start_pos == Position(4, 0 if is_white else 7):
                self.__castlings = self.__castlings.replace("Q" if is_white else "q", "")
                self.__castlings = self.__castlings.replace("K" if is_white else "k", "")

                if move.end_pos.col == 2:
                    start_pos = Position(0, move.end_pos.row)
                    end_pos = move.end_pos + (1, 0)
                    self.__board.make_move(Move(start_pos, end_pos))
                elif move.end_pos.col == 6:
                    start_pos = Position(7, move.end_pos.row)
                    end_pos = move.end_pos + (-1, 0)
                    self.__board.make_move(Move(start_pos, end_pos))

        def get_new_state() -> State:
            can_make_move = False
            for p in self.__board.pieces_pos.keys():
                if p.is_white is self.__is_white_turn and len(self.get_legal_piece_pos(p)) > 0:
                    can_make_move = True
                    break

            if not can_make_move:
                if ChessRules.king_is_under_atk(self, self.__is_white_turn):
                    return State.WIN_B if self.__is_white_turn else State.WIN_W
                else:
                    return State.DRAW

            elif self.__halfclock >= 100:
                return State.DRAW

            return State.IN_PROGRESS

        if not is_test and not ChessRules.is_legal_move(self, move):
            return

        should_reset_halfclock = self.__board[move.end_pos] is not None

        # Update self.__board
        piece = self.__board.make_move(move)

        # Update self.__castlings and self.__en_passants
        e_p_target = None
        if isinstance(piece, Rook):
            rook_actions(piece.is_white)
        elif isinstance(piece, King):
            king_actions(piece.is_white)
        elif isinstance(piece, Pawn):
            should_reset_halfclock = True
            e_p_target = pawn_actions(piece.is_white)
        self.__en_passant_target = e_p_target

        # Update self.__is_white_turn
        self.__is_white_turn = not self.__is_white_turn

        # Update self.__halfclock
        self.__halfclock = 0 if should_reset_halfclock else self.__halfclock + 1

        # Update self.__fullclock
        if self.__is_white_turn:
            self.__fullclock += 1

        # Update self.__moves_played
        self.__played_moves.append(move)

        if not is_test:
            # Update self.__state
            self.__state = get_new_state()

        # Reset self.__possible_poss
        self.__legal_pieces_pos.clear()