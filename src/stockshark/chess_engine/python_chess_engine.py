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
        return self._board.piece_at(chess.parse_square(tile))

    def _gen_attacked_tiles(self) -> Set[str]:
        attacking_color = not self._board.turn
        attacked_tiles = set()
        for square in chess.SQUARES:
            if self._board.is_attacked_by(attacking_color, square):
                attacked_tiles.add(chess.square_name(square))
        return attacked_tiles

    def is_tile_attacked(self, tile, is_white_attacking):
        attacking_color = chess.WHITE if is_white_attacking else chess.BLACK
        square = chess.parse_square(tile)
        return self._board.is_attacked_by(attacking_color, square)
