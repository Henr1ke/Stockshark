from typing import List, Optional

from stockshark.chess_engine.board import Board
from stockshark.chess_engine_2.chess_engine import ChessEngine
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class StocksharkEngine(ChessEngine):

    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        fen_fields = fen.split(" ")
        self.__board: Board = Board(fen_fields[0])
        self.__is_white_turn: bool = True if fen_fields[1] == "w" else False
        self.__castlings: str = fen_fields[2]
        self.__en_passant_target: Optional[Tile] = None if fen_fields[3] == "-" else Tile(fen_fields[3])
        self.__halfclock: int = int(fen_fields[4])
        self.__fullclock: int = int(fen_fields[5])

    def make_move(self, move: Move) -> bool:
        pass

    def get_available_moves(self) -> List[Move]:
        pass

    def _gen_fen(self) -> str:
        pass


if __name__ == '__main__':
    game = StocksharkEngine()
