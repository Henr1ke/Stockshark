from __future__ import annotations
from typing import List

from stockshark.chess_engine_2.chess_engine import ChessEngine

from chess import Move as ChessMove, Board as ChessBoard


class PythonChessEngine(ChessEngine):
    def _new_game(self, fen: str):
        self._board = ChessBoard(fen)

    def _make_move(self, move: str) -> None:
        chess_move = ChessMove.from_uci(move)
        self._board.push(chess_move)

    def _gen_available_moves(self) -> List[str]:
        return [move.uci() for move in self._board.legal_moves]

    def _gen_fen(self) -> str:
        return self._board.fen()

