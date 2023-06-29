from typing import List

from stockshark.chess_engine_2.chess_engine import ChessEngine
from stockshark.chess_engine_2.stockfish_dao import StockfishDao


class StockfishEngine(ChessEngine):

    def _new_game(self, fen: str):
        self._sf_dao: StockfishDao = StockfishDao()
        self._sf_dao.new_game(fen)

    def _make_move(self, move: str) -> None:
        self._sf_dao.make_move(self.fen, move)

    def _gen_available_moves(self) -> List[str]:
        return self._sf_dao.get_available_moves()

    def _gen_fen(self) -> str:
        return self._sf_dao.get_fen()
