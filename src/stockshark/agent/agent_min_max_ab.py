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


class AgentMinMaxAB(Agent):
    CHECK_VALUE = 90
    TIMES = []

    def __init__(self, depth: int = 4):
        if depth <= 0:
            raise ValueError("Depth can not be less or equal to zero")

        self.__depth = depth

    def gen_move(self, engine: ChessEngine) -> str:
        ti = time.time_ns()
        _, moves = self.minmax_ab(self.__depth, engine)
        AgentMinMaxAB.TIMES.append(time.time_ns() - ti)
        return random.choice(moves)

    def minmax_ab(self, max_depth: int, engine: ChessEngine, curr_depth: int = 0, alpha: float = -math.inf,
                  beta: float = math.inf) -> Tuple[float, List[str]]:
        is_white_turn = engine.fen.split()[1] == 'w'

        moves_info = []
        for move in engine.available_moves:
            engine_copy = copy(engine)
            engine_copy.play(move)
            moves_info.append((move, engine_copy, AgentMinMaxAB.evaluate_game(engine_copy)))
        moves_info.sort(reverse=is_white_turn, key=lambda move_info: move_info[2])

        best_val, best_moves = -math.inf if is_white_turn else math.inf, []
        for move, engine_copy, value in moves_info:
            if curr_depth + 1 < max_depth:
                value, _ = self.minmax_ab(max_depth, engine_copy, curr_depth + 1, alpha, beta)

            if value == best_val:
                best_moves.append(move)
            elif is_white_turn:
                if value > best_val:
                    best_val = value
                    alpha = max(alpha, best_val)
                    best_moves = [move]
            else:
                if value < best_val:
                    best_val = value
                    beta = min(beta, best_val)
                    best_moves = [move]

            if beta <= alpha:
                break

        return best_val, best_moves

    @staticmethod
    def evaluate_game(engine: ChessEngine) -> float:
        value = 0
        is_white_turn = engine.fen.split(" ")[1] == "w"
        if engine.is_in_check(is_white_turn):
            if engine.game_finished():
                return -math.inf if is_white_turn else math.inf
            else:
                value += -AgentMinMaxAB.CHECK_VALUE if is_white_turn else AgentMinMaxAB.CHECK_VALUE

        fen = engine.fen.split(" ")[0]
        for char in fen:
            try:
                piece_value = Piece.get_piece_value(char)
                value += piece_value if char.isupper() else -piece_value
            except ValueError:
                continue
        return value

    @staticmethod
    def evaluate_move(engine: ChessEngine, move: str) -> float:
        start_tile = move[:2]
        end_tile = move[2:4]
        moved_piece = engine.get_piece_at(start_tile)
        eaten_piece = engine.get_piece_at(end_tile)

        value = 0
        if len(move) == 5:
            promoted_piece = move[4]
            if promoted_piece == Piece.QUEEN_B:
                value += Piece.QUEEN_VALUE
            elif promoted_piece == Piece.ROOK_B:
                value += Piece.ROOK_VALUE
            elif promoted_piece == Piece.BISHOP_B:
                value += Piece.BISHOP_VALUE
            elif promoted_piece == Piece.KNIGHT_B:
                value += Piece.KNIGHT_VALUE
            value = value if moved_piece.isupper() else -value

        if eaten_piece is None:
            return value
        try:
            piece_value = Piece.get_piece_value(eaten_piece)
            value += -piece_value if eaten_piece.isupper() else piece_value
            return value
        except ValueError:
            return value


if __name__ == '__main__':
    fen = "6R1/6p1/1P1p1kN1/2Pb1P2/P7/5p2/4p1n1/1n4KR w - - 0 1"
    # fen = "1r2r1k1/5ppp/8/q1b3n1/3P3P/2P2BP1/PPN2P2/3KQ2R w - - 0 1"
    # fen = "k2bn1b1/1p3n1r/8/8/3N4/8/2r5/K7 b - - 0 1"
    # fen = "r1Nbn1bk/1p3n2/8/8/1B6/2R5/1r6/7K b - - 0 1"
    engine = PythonChessEngine(fen)

    vis = Visualizer(Visualizer.CHARSET_LETTER)
    vis.show(engine)

    p_mm = AgentMinMaxAB(4)
    ti = time.time()
    move = p_mm.gen_move(engine)
    print(time.time() - ti)
    print(move)

    # move = "e8e1"
    # print(AgentMinMaxAB.evaluate_move(engine, move))
