import math
import time
from copy import copy
from typing import Tuple

from stockshark.agent.agent import Agent
from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.chess_engine.stockshark_engine import StocksharkEngine
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
        _, move = self.minmax(self.__depth, engine)
        AgentMinMax.TIMES.append(time.time_ns() - ti)
        return move

    def minmax(self, max_depth: int, engine: ChessEngine, curr_depth: int = 0) -> Tuple[float, Move]:
        moves = engine.available_moves

        is_white_turn = engine.fen.split(" ")[1] == "w"
        best_val, best_move = -math.inf if is_white_turn else math.inf, None
        for move in moves:
            game_copy = copy(engine)
            game_copy.play(move)

            if curr_depth + 1 == max_depth:
                value = game_copy.evaluate_game()
            else:
                value, _ = self.minmax(max_depth, game_copy, curr_depth + 1)

            if engine.is_white_turn:
                if value > best_val:
                    best_val = value
                    best_move = move
            else:
                if value < best_val:
                    best_val = value
                    best_move = move

        return best_val, best_move

    @staticmethod
    def evaluate_game(fen):
        value = 0
        for char in fen.split(" ")[0]:
            if char == "P":
                value += 1
            elif char == "N":
                value += 3
            elif char == "B":
                value += 3
            elif char == "R":
                value += 5
            elif char == "Q":
                value += 9
            elif char == "p":
                value -= 1
            elif char == "n":
                value -= 3
            elif char == "b":
                value -= 3
            elif char == "r":
                value -= 5
            elif char == "q":
                value -= 9
        return value

    def evaluate_move(self, move: Move) -> float:
        eaten_piece = self.__board[move.end_pos]
        return 0 if eaten_piece is None else eaten_piece.value


if __name__ == '__main__':
    game = StocksharkEngine("1r2r1k1/5ppp/8/q1b3n1/3P3P/2P2BP1/PPN2P2/3KQ2R w - - 0 1")

    vis = Visualizer(Visualizer.CHARSET_LETTER)
    vis.show(game)

    p_mm = AgentMinMax()
    move = p_mm.gen_move(game)
    print(move)
