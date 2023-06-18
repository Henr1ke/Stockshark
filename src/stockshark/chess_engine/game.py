from __future__ import annotations

from copy import copy
from typing import Dict, Optional, List, Tuple

from stockshark.piece.king import King
from stockshark.piece.pawn import Pawn
from stockshark.piece.piece import Piece
from stockshark.piece.queen import Queen
from stockshark.piece.rook import Rook
from stockshark.chess_engine.board import Board
from stockshark.chess_engine.game_rules import GameRules
from stockshark.chess_engine.state import State
from stockshark.util.move import Move
from stockshark.util.position import Position


class Game:
    def __init__(self, fen_str: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
        fen_str_fields = fen_str.split()

        self.__board: Board = Board(fen_str_fields[0])
        self.__is_white_turn: bool = True if fen_str_fields[1] == "w" else False
        self.__castlings: str = fen_str_fields[2]
        self.__en_passant_target: Optional[Position] = None if fen_str_fields[3] == "-" else Position(fen_str_fields[3])
        self.__halfclock: int = int(fen_str_fields[4])
        self.__fullclock: int = int(fen_str_fields[5])
        self.__played_moves: List[Move] = []
        self.__legal_piece_moves: Dict[Piece, List[Move]] = dict()
        self.__state: State = State.IN_PROGRESS

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

    def __copy__(self) -> Game:
        cls = self.__class__
        game = cls.__new__(cls)
        for key, value in self.__dict__.items():
            if key == "_Game__legal_piece_moves":
                legal_piece_moves = {piece: copy(moves) for piece, moves in self.__legal_piece_moves.items()}
                setattr(game, key, legal_piece_moves)
            else:
                setattr(game, key, copy(value))
        return game

    def get_available_pieces_pos(self) -> Dict[Piece, Position]:
        return {piece: pos for piece, pos in self.__board.pieces_pos.items()
                if piece.is_white is self.__is_white_turn and len(self.get_legal_piece_moves(piece)) > 0}

    def get_legal_piece_moves(self, piece: Piece) -> List[Move]:
        if piece not in self.__legal_piece_moves:
            moves = piece.gen_moves(self)

            legal_moves = [move for move in moves if not GameRules.leaves_king_under_atk(self, move)]

            # Updates the dictionary
            self.__legal_piece_moves[piece] = legal_moves

        return self.__legal_piece_moves[piece]

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

    def evaluate_game(self) -> float:
        value = 0
        for piece in self.__board.pieces_pos.keys():
            value += piece.value if piece.is_white else -piece.value
        return value

    def evaluate_move(self, move: Move) -> float:
        eaten_piece = self.__board[move.end_pos]
        return 0 if eaten_piece is None else eaten_piece.value

    def __pawn_actions(self, move: Move) -> Optional[Position]:
        piece = self.__board[move.end_pos]
        if move.end_pos == self.__en_passant_target:
            capt_piece_pos = move.end_pos + ((0, -1) if piece.is_white else (0, 1))
            self.__board.clear_pos(capt_piece_pos)
        elif move.end_pos.row == (7 if piece.is_white else 0):
            self.__board.add_piece(Queen(piece.is_white), move.end_pos)  # TODO its always promoting to queen

        if abs(move.start_pos.row - move.end_pos.row) == 2:
            return move.end_pos + ((0, -1) if piece.is_white else (0, 1))

    def __rook_actions(self, move: Move) -> None:
        piece = self.__board[move.end_pos]
        initial_row = 0 if piece.is_white else 7
        if move.start_pos.row == initial_row:
            if move.start_pos.col == 0:
                self.__castlings = self.__castlings.replace("Q" if piece.is_white else "q", "")
            elif move.start_pos.col == 7:
                self.__castlings = self.__castlings.replace("K" if piece.is_white else "k", "")

    def __king_actions(self, move: Move) -> None:
        piece = self.__board[move.end_pos]
        if move.start_pos == Position(4, 0 if piece.is_white else 7):
            self.__castlings = self.__castlings.replace("Q" if piece.is_white else "q", "")
            self.__castlings = self.__castlings.replace("K" if piece.is_white else "k", "")

            if move.end_pos.col == 2:
                start_pos = Position(0, move.end_pos.row)
                end_pos = move.end_pos + (1, 0)
                self.__board.make_move(Move(start_pos, end_pos))
            elif move.end_pos.col == 6:
                start_pos = Position(7, move.end_pos.row)
                end_pos = move.end_pos + (-1, 0)
                self.__board.make_move(Move(start_pos, end_pos))

    def __get_new_state(self) -> State:
        can_make_move = False
        for p in self.__board.pieces_pos.keys():
            if p.is_white is self.__is_white_turn and len(self.get_legal_piece_moves(p)) > 0:
                can_make_move = True
                break

        if not can_make_move:
            if GameRules.king_is_under_atk(self, self.__is_white_turn):
                return State.WIN_B if self.__is_white_turn else State.WIN_W
            else:
                return State.DRAW

        elif self.__halfclock >= 100:
            return State.DRAW

        return State.IN_PROGRESS

    def make_move(self, move: Move, is_test=False) -> bool:
        piece = self.__board[move.start_pos]
        if not is_test and GameRules.is_legal(self, move):
            return False

        eaten_piece = self.__board[move.end_pos]
        should_reset_halfclock = eaten_piece is not None

        # Update self.__board
        self.__board.make_move(move)

        # Update self.__castlings and self.__en_passants
        e_p_target = None
        if isinstance(piece, Rook):
            self.__rook_actions(move)
        elif isinstance(piece, King):
            self.__king_actions(move)
        elif isinstance(piece, Pawn):
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

        if not is_test:
            # Update self.__state
            self.__state = self.__get_new_state()

        # Update self.__moves_played
        self.__played_moves.append(move)

        # Reset self.__possible_poss
        self.__legal_piece_moves.clear()

        return True
