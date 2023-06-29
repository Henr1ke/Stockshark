import random
from typing import List

from stockshark.chess_engine_2.chess_engine import ChessEngine

from chess import Move as ChessMove, Board as ChessBoard

from stockshark.util.move import Move


class ChessPackageEngine(ChessEngine):

    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self._board = ChessBoard(fen)
        super().__init__()

    def make_move(self, move: Move) -> bool:
        chess_move = ChessMove.from_uci(move.to_uci())
        self._board.push(chess_move)
        return super().make_move(move)

    def get_available_moves(self) -> List[Move]:
        return [Move.from_uci(move.uci()) for move in self._board.legal_moves]

    def _gen_fen(self) -> str:
        return self._board.fen()


