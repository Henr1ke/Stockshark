import math
import time
from copy import copy
import heapq
from typing import Tuple, Dict, Type, List, Optional

from chess.piece.bishop import Bishop
from chess.piece.king import King
from chess.piece.knight import Knight
from chess.piece.pawn import Pawn
from chess.piece.piece import Piece
from chess.piece.queen import Queen
from chess.piece.rook import Rook
from chess.player.player import Player
from chess.chessGame.chess_game import ChessGame
from chess.sim.visualizer import Visualizer
from chess.util.move import Move


class PlayerMinMax(Player):
    PIECES_VALUES: Dict[Type[Piece], float] = {Pawn: 100, Knight: 300, Bishop: 300, Rook: 500, Queen: 900, King: 3000}

    def gen_move(self, game: ChessGame) -> Move:
        pass

    def evaluate_game(self, game: ChessGame) -> float:
        value = 0

        pieces_pos = game.board.pieces_pos
        for piece in pieces_pos.keys():
            piece_val = PlayerMinMax.PIECES_VALUES[type(piece)]
            value += piece_val if piece.is_white else -piece_val
        return value

    def minmax(self, curr_depth: int, max_depth: int, game: ChessGame) -> Tuple[float, Move]:
        moves = game.legal_moves

        best_val, best_move = -math.inf if game.is_white_turn else math.inf, None
        for move in moves:
            game_copy = copy(game)
            game_copy.play(move)

            if curr_depth + 1 == max_depth:
                value = self.evaluate_game(game_copy)
            else:
                value, _ = self.minmax(curr_depth + 1, max_depth, game_copy)

            if game.is_white_turn:
                if value > best_val:
                    best_val = value
                    best_move = move
            else:
                if value < best_val:
                    best_val = value
                    best_move = move

        return best_val, best_move

    def minmax_ab(self, curr_depth: int, max_depth: int, game: ChessGame, alpha: float = -math.inf,
                  beta: float = math.inf) -> Tuple[float, Move]:
        moves = game.legal_moves

        best_val, best_move = -math.inf if game.is_white_turn else math.inf, None
        for move in moves:
            game_copy = copy(game)
            game_copy.play(move)

            if curr_depth + 1 == max_depth:
                value = self.evaluate_game(game_copy)
            else:
                value, _ = self.minmax_ab(curr_depth + 1, max_depth, game_copy, alpha, beta)

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

    def minmax_ab_sorted(self, curr_depth: int, max_depth: int, game: ChessGame, alpha: float = -math.inf,
                         beta: float = math.inf) -> Tuple[float, Move]:
        moves = game.legal_moves

        moves.sort(reverse=not game.is_white_turn)

        best_val, best_move = -math.inf if game.is_white_turn else math.inf, None
        for move in moves:
            game_copy = copy(game)
            game_copy.play(move)

            if curr_depth + 1 == max_depth:
                value = self.evaluate_game(game_copy)
            else:
                value, _ = self.minmax_ab_sorted(curr_depth + 1, max_depth, game_copy, alpha, beta)

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
    game = ChessGame("1r2r1k1/5ppp/8/q1b3n1/3P3P/2P2BP1/PPN2P2/3KQ2R w - - 0 1")

    vis = Visualizer(Visualizer.CHARSET_LETTER)
    vis.show(game)

    p_mm = PlayerMinMax()
    depth = 2

    ti = time.time()
    val, move = p_mm.minmax_ab_sorted(0, depth, game)
    tf = time.time()
    print("minmax alpha beta sorting moves:")
    print(f"result: {val, move}")
    print(f"duration: {round(tf - ti, 3)}s")
    print()

    ti = time.time()
    val, move = p_mm.minmax_ab(0, depth, game)
    tf = time.time()
    print("minmax alpha beta:")
    print(f"result: {val, move}")
    print(f"duration: {round(tf - ti, 3)}s")
    print()

    ti = time.time()
    val, move = p_mm.minmax(0, depth, game)
    tf = time.time()
    print("basic minmax:")
    print(f"result: {val, move}")
    print(f"duration: {round(tf - ti, 3)}s")