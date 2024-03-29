from __future__ import annotations

from typing import Optional, Set

import chess
from chess import Move as ChessMove, Board as ChessBoard

from stockshark.chess_engine.chess_engine import ChessEngine


class PythonChessEngine(ChessEngine):

    def _new_game(self, fen: str):
        self._board = ChessBoard(fen)

    def _make_move(self, move: str) -> None:
        chess_move = ChessMove.from_uci(move)
        self._board.push(chess_move)

    def _gen_available_moves(self) -> Set[str]:
        return {move.uci() for move in self._board.legal_moves}

    def _gen_fen(self) -> str:
        return self._board.fen()

    def get_piece_at(self, tile: str) -> Optional[str]:
        piece = self._board.piece_at(chess.parse_square(tile))
        return None if piece is None else piece.symbol()

    def is_in_check(self, is_white_side: bool) -> bool:
        return self._board.is_check() and self._board.turn == (chess.WHITE if is_white_side else chess.BLACK)
