import math
import random
import time
from copy import copy
from typing import Tuple, List

from stockshark.agent.agent import Agent
from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.chess_engine.python_chess_engine import PythonChessEngine
from stockshark.piece.piece import Piece
from stockshark.sim.visualizer import Visualizer


class AgentMinMax(Agent):
    CHECK_VALUE = 90
    TIMES = []

    def __init__(self, depth: int = 4):
        if depth <= 0:
            raise ValueError("Depth can not be less or equal to zero")

        self.__depth = depth

    def gen_move(self, engine: ChessEngine) -> str:
        ti = time.time_ns()
        _, moves = self.minmax(self.__depth, engine)
        AgentMinMax.TIMES.append(time.time_ns() - ti)
        return random.choice(moves)

    def minmax(self, max_depth: int, engine: ChessEngine, curr_depth: int = 0) -> Tuple[float, List[str]]:
        is_white_turn = engine.fen.split()[1] == 'w'

        moves_info = []
        for move in engine.available_moves:
            engine_copy = copy(engine)
            engine_copy.play(move)
            moves_info.append((move, engine_copy, AgentMinMax.evaluate_game(engine_copy)))
        moves_info.sort(reverse=is_white_turn, key=lambda move_info: move_info[2])

        best_val, best_moves = -math.inf if is_white_turn else math.inf, []
        for move, engine_copy, value in moves_info:
            if curr_depth + 1 < max_depth:
                value, _ = self.minmax(max_depth, engine_copy, curr_depth + 1)

            if value == best_val:
                best_moves.append(move)
            elif is_white_turn:
                if value > best_val:
                    best_val = value
                    best_moves = [move]
            else:
                if value < best_val:
                    best_val = value
                    best_moves = [move]

        return best_val, best_moves

    @staticmethod
    def evaluate_game(engine: ChessEngine) -> float:
        value = 0
        is_white_turn = engine.fen.split(" ")[1] == "w"
        if engine.is_in_check(is_white_turn):
            if engine.game_finished():
                return -math.inf if is_white_turn else math.inf
            else:
                value += -AgentMinMax.CHECK_VALUE if is_white_turn else AgentMinMax.CHECK_VALUE

        fen = engine.fen.split(" ")[0]
        for char in fen:
            try:
                piece_value = Piece.get_piece_value(char)
                value += piece_value if char.isupper() else -piece_value
            except ValueError:
                continue
        return value


if __name__ == '__main__':
    engine = PythonChessEngine("1r2r1k1/5ppp/8/q1b3n1/3P3P/2P2BP1/PPN2P2/3KQ2R w - - 0 1")

    vis = Visualizer(Visualizer.CHARSET_LETTER)
    vis.show(engine)

    p_mm = AgentMinMax()
    move = p_mm.gen_move(engine)
    print(move)
