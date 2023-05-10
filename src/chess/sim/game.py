from copy import copy
from typing import Dict, Optional, List

from chess.piece.piece import Piece
from chess.sim.board import Board
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

    def play(self, move: Move) -> None:
        pass

    # def get_legal_piece_pos(self, piece: Piece) -> List[Position]:
    #     legal_pos = self.__legal_pieces_pos.get(piece)
    #
    #     if legal_pos is None:
    #         possible_pos = piece.gen_positions(self.__board, self.__board.)
    #
    #         if isinstance(piece, Pawn):
    #             # Adds en passant target to the possible positions if possible
    #             increments = ((-1, 1), (-1, 1)) if piece.is_white else ((1, -1), (-1, -1))
    #             for inc in increments:
    #                 try:
    #                     end_pos = start_pos + inc
    #                     if end_pos == self.__en_passant_target:
    #                         possible_pos.append(end_pos)
    #                         break
    #                 except ChessException:
    #                     pass
    #
    #         if isinstance(piece, King):
    #             # Adds castling positions to the possible positions if possible
    #             castling_rights = self.get_castlings(piece.is_white)
    #             if castling_rights[0] and self.__board[1, start_pos.row] is None and \
    #                     self.__board[2, start_pos.row] is None and self.__board[3, start_pos.row] is None:
    #                 possible_pos.append(start_pos + (-2, 0))
    #             if castling_rights[1] and self.__board[5, start_pos.row] is None and \
    #                     self.__board[6, start_pos.row] is None:
    #                 possible_pos.append(start_pos + (2, 0))
    #
    #         # Only keeps the position if the move does not leave the king in check
    #         legal_pos = [end_pos for end_pos in possible_pos
    #                      if not self.__leaves_king_under_atk(Move(start_pos, end_pos), piece.is_white)]
    #
    #         # Updates the dictionary
    #         self.__pieces_positions[piece] = legal_pos
    #
    #     return legal_pos
