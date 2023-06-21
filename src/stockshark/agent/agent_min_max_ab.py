import math
from copy import copy
from typing import Tuple

from stockshark.agent.agent import Agent
from stockshark.chess_engine.game_engine import GameEngine
from stockshark.chess_engine.stockshark_engine import StockSharkEngine
from stockshark.sim.visualizer import Visualizer
from stockshark.util.move import Move


class AgentMinMaxAB(Agent):
    def gen_move(self, game: GameEngine) -> Move:
        _, move = self.minmax_ab(3, game)
        return move

    def minmax_ab(self, max_depth: int, game: GameEngine, curr_depth: int = 0, alpha: float = -math.inf,
                  beta: float = math.inf) -> Tuple[float, Move]:
        # moves = game.legal_moves
        moves = []
        pieces_tiles = game.get_available_pieces_tiles()
        for piece in pieces_tiles.keys():
            moves += game.get_legal_piece_moves(piece)

        moves.sort(reverse=not game.is_white_turn, key=game.evaluate_move)

        best_val, best_move = -math.inf if game.is_white_turn else math.inf, None
        for move in moves:
            game_copy = copy(game)
            game_copy.make_move(move)

            if curr_depth + 1 == max_depth:
                value = game_copy.evaluate_game()
            else:
                value, _ = self.minmax_ab(max_depth, game_copy, curr_depth + 1, alpha, beta)

            if game.is_white_turn:
                if value > best_val:
                    best_val = value
                    best_move = move
                    alpha = max(alpha, best_val)
            else:
                if value < best_val:
                    best_val = value
                    best_move = move
                    beta = min(beta, best_val)

            if beta <= alpha:
                break

        return best_val, best_move


if __name__ == '__main__':
    game = StockSharkEngine("1r2r1k1/5ppp/8/q1b3n1/3P3P/2P2BP1/PPN2P2/3KQ2R w - - 0 1")

    vis = Visualizer(Visualizer.CHARSET_LETTER)
    vis.show(game)

    p_mm = AgentMinMaxAB()
    move = p_mm.gen_move(game)
    print(move)
