import math
import time
from copy import copy
from typing import Tuple

from stockshark.agent.agent import Agent
from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.chess_engine.stockshark_engine import StocksharkEngine
from stockshark.piece.piece import Piece
from stockshark.sim.visualizer import Visualizer
from stockshark.util.move import Move


class AgentMinMax(Agent):
    TIMES = []

    def __init__(self, depth: int = 2):
        if depth <= 0:
            raise ValueError("Depth can not be less or equal to zero")

        self.__depth = depth

    def gen_move(self, engine: ChessEngine) -> Move:
        ti = time.time_ns()
        _, move_str = self.minmax(self.__depth, engine)
        AgentMinMax.TIMES.append(time.time_ns() - ti)
        return Move.from_uci(move_str)

    def minmax(self, max_depth: int, engine: ChessEngine, curr_depth: int = 0) -> Tuple[float, str]:
        moves = engine.available_moves

        is_white_turn = engine.fen.split(" ")[1] == "w"
        best_val, best_move = -math.inf if is_white_turn else math.inf, None
        for move in moves:
            game_copy = copy(engine)
            game_copy.play(move)

            if curr_depth + 1 == max_depth:
                value = AgentMinMax.evaluate_game()
            else:
                value, _ = self.minmax(max_depth, game_copy, curr_depth + 1)

            if is_white_turn:
                if value > best_val:
                    best_val = value
                    best_move = move
            else:
                if value < best_val:
                    best_val = value
                    best_move = move

        return best_val, best_move

    @staticmethod
    def evaluate_game(engine: ChessEngine) -> float:
        value = 0
        for char in engine.fen.split(" ")[0]:
            if char == Piece.PAWN_W:
                value += Piece.PAWN_VALUE
            elif char == Piece.PAWN_B:
                value -= Piece.PAWN_VALUE
            elif char == Piece.KNIGHT_W:
                value += Piece.KNIGHT_VALUE
            elif char == Piece.KNIGHT_B:
                value -= Piece.KNIGHT_VALUE
            elif char == Piece.BISHOP_W:
                value += Piece.BISHOP_VALUE
            elif char == Piece.BISHOP_B:
                value -= Piece.BISHOP_VALUE
            elif char == Piece.ROOK_W:
                value += Piece.ROOK_VALUE
            elif char == Piece.ROOK_B:
                value -= Piece.ROOK_VALUE
            elif char == Piece.QUEEN_W:
                value += Piece.QUEEN_VALUE
            elif char == Piece.QUEEN_B:
                value -= Piece.QUEEN_VALUE
        return value

    @staticmethod
    def evaluate_move(engine: ChessEngine, move: str) -> float:
        end_tile = move[2:4]
        eaten_piece = engine.get_piece_at(end_tile)

        if eaten_piece is None:
            return 0
        elif eaten_piece == Piece.PAWN_W:
            return Piece.PAWN_VALUE
        elif eaten_piece == Piece.PAWN_B:
            return -Piece.PAWN_VALUE
        elif eaten_piece == Piece.KNIGHT_W:
            return Piece.KNIGHT_VALUE
        elif eaten_piece == Piece.KNIGHT_B:
            return -Piece.KNIGHT_VALUE
        elif eaten_piece == Piece.BISHOP_W:
            return Piece.BISHOP_VALUE
        elif eaten_piece == Piece.BISHOP_B:
            return -Piece.BISHOP_VALUE
        elif eaten_piece == Piece.ROOK_W:
            return Piece.ROOK_VALUE
        elif eaten_piece == Piece.ROOK_B:
            return -Piece.ROOK_VALUE
        elif eaten_piece == Piece.QUEEN_W:
            return Piece.QUEEN_VALUE
        elif eaten_piece == Piece.QUEEN_B:
            return -Piece.QUEEN_VALUE
        return 0


if __name__ == '__main__':
    game = StocksharkEngine("1r2r1k1/5ppp/8/q1b3n1/3P3P/2P2BP1/PPN2P2/3KQ2R w - - 0 1")

    vis = Visualizer(Visualizer.CHARSET_LETTER)
    vis.show(game)

    p_mm = AgentMinMax()
    move = p_mm.gen_move(game)
    print(move)
