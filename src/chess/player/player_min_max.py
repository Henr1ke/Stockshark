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
        moves = []
        pieces_pos = game.get_available_pieces_pos()
        for piece, start_pos in pieces_pos.items():
            positions = game.get_legal_piece_pos(piece)
            for end_pos in positions:
                move = Move(start_pos, end_pos)
                game_copy = copy(game)
                game_copy.play(move)

                if curr_depth + 1 >= max_depth:
                    value = self.evaluate_game(game_copy)
                else:
                    value, _ = self.minmax(curr_depth + 1, max_depth, game_copy)
                heapq.heappush(moves, (value, move))

        value, move = heapq.nlargest(1, moves)[0] if game.is_white_turn else heapq.nsmallest(1, moves)[0]
        return value, move

    def minmax_ab(self, curr_depth: int, max_depth: int, game: ChessGame, alpha: float = -math.inf,
                  beta: float = math.inf) -> Tuple[float, Move]:
        best_val, best_move = -math.inf if game.is_white_turn else math.inf, None

        moves = []
        pieces_pos = game.get_available_pieces_pos()
        for piece, start_pos in pieces_pos.items():
            positions = game.get_legal_piece_pos(piece)
            moves += [Move(start_pos, end_pos) for end_pos in positions]

        # moves.sort(reverse=game.is_white_turn)
        # TODO quando os moves tiverem o eaten_piece atribuido vai dar pra fazer sort

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


if __name__ == '__main__':
    # # A simple Python3 program to find
    # # maximum score that
    # # maximizing player can get
    # import math
    #
    #
    # def minimax(curDepth, nodeIndex, maxTurn, scores, targetDepth):
    #
    #     # base case : targetDepth reached
    #     if curDepth == targetDepth:
    #         return scores[nodeIndex]
    #
    #     val1 = minimax(curDepth + 1, nodeIndex * 2, not maxTurn, scores, targetDepth)
    #     val2 = minimax(curDepth + 1, nodeIndex * 2 + 1, not maxTurn, scores, targetDepth)
    #
    #     return max(val1, val2) if maxTurn else min(val1, val2)
    #
    #
    # # Driver code
    # scores = [3, 5, 2, 9, 12, 5, 23, 23]
    #
    # treeDepth = math.log(len(scores), 2)
    #
    # print("The optimal value is : ", end="")
    # print(minimax(0, 0, True, scores, treeDepth))

    # This code is contributed
    # by rootshadow

    game = ChessGame("1r2r1k1/5ppp/8/q1b3n1/3P3P/2P2BP1/PPN2P2/3KQ2R w - - 0 1")

    vis = Visualizer(Visualizer.W_PIECE_CHARSET_LETTER, Visualizer.B_PIECE_CHARSET_LETTER)
    vis.show(game)

    p_mm = PlayerMinMax()
    depth = 3

    ti = time.time()
    # val, move = p_mm.minmax(0, depth, game)
    val, move = p_mm.minmax_ab(0, depth, game)
    tf = time.time()

    print(val)
    print(move)
    print(tf - ti)
