from copy import copy
from typing import Dict, Optional, List

from chess.piece.piece import Piece
from chess.sim.board import Board
from chess.sim.gameRules import GameRules
from chess.util.move import Move
from chess.util.position import Position


class Game:
    def __init__(self, fen_str: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
        fen_str_fields = fen_str.split()

        self.__board: Board = Board(fen_str_fields[0])

        self.__is_white_turn: bool = True if fen_str_fields[1] == "w" else False

        self.__castlings: str = fen_str_fields[2]

        self.__en_passant_target: Optional[Position] = None if fen_str_fields[3] == "-" else Position(fen_str_fields[3])

        self.__halfclock: int = int(fen_str_fields[4])
        self.__fullclock: int = int(fen_str_fields[5])

        self.__moves_played: List[Move] = []

        self.__legal_pieces_pos: Dict[Piece, List[Position]] = dict()

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
    def moves_played(self) -> List[Move]:
        return copy(self.__moves_played)

    def gen_fen_str(self):
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
            start_pos = self.__board.pieces_pos[piece]
            possible_pos = piece.gen_positions(self)

            # Only keeps the position if the move does not leave the king in check
            legal_pos = [end_pos for end_pos in possible_pos
                         if not GameRules.leaves_king_under_atk(self, Move(start_pos, end_pos))]

            # Updates the dictionary
            self.__legal_pieces_pos[piece] = legal_pos

        return self.__legal_pieces_pos[piece]

    def play(self, move: Move) -> None:
        pass
