from __future__ import annotations

from typing import Optional, Set

import chess
from chess import Move as ChessMove, Board as ChessBoard

from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class PythonChessEngine(ChessEngine):

    def _new_game(self, fen: str):
        self._board = ChessBoard(fen)

    def _make_move(self, move: Move) -> None:
        chess_move = ChessMove.from_uci(move.to_uci())
        self._board.push(chess_move)

    def _gen_available_moves(self) -> Set[Move]:
        return {Move.from_uci(move.uci()) for move in self._board.legal_moves}

    def _gen_fen(self) -> str:
        return self._board.fen()

    def get_piece_at(self, tile: Tile) -> Optional[str]:
        return self._board.piece_at(chess.parse_square(tile.name))

    def _gen_attacked_tiles(self) -> Set[Tile]:
        attacking_color = not self._board.turn
        attacked_tiles = set()
        for square in chess.SQUARES:
            if self._board.is_attacked_by(attacking_color, square):
                attacked_tiles.add(Tile(chess.square_name(square)))
        return attacked_tiles

    def is_in_check(self, is_white_side: bool) -> bool:
        return self._board.is_check() and self._board.turn == chess.WHITE if is_white_side else chess.BLACK
