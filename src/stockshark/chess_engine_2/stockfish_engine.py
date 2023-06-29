
from typing import List

from stockshark.chess_engine_2.chess_engine import ChessEngine
from stockshark.chess_engine_2.stockfish_dao import StockfishDao


class StockfishEngine(ChessEngine):

    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self._sf_dao: StockfishDao = StockfishDao()
        self._sf_dao.new_game(fen)
        super().__init__()

    def make_move(self, move: str) -> bool:
        self._sf_dao.make_move(self.fen, move)
        return super().make_move(move)

    def get_available_moves(self) -> List[str]:
        return self._sf_dao.get_available_moves()

    def _gen_fen(self) -> str:
        return self._sf_dao.get_fen()


