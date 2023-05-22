import random
from typing import Optional

from heapq import heappop, heappush

from chess.chessGame.chess_game import ChessGame
from chess.player.behaviour.behaviour import Behaviour
from chess.util.move import Move


class EatBehaviour(Behaviour):

    def gen_move(self, game: ChessGame) -> Optional[Move]:
        actions = []

        pieces_pos = game.get_available_pieces_pos()
        board = game.board

        for piece, start_pos in pieces_pos.items():
            piece_pos = game.get_legal_piece_pos(piece)
            for end_pos in piece_pos:
                attacked_piece = board[end_pos]
                if attacked_piece is not None:
                    move = Move(start_pos, end_pos)
                    prio = -EatBehaviour.get_prio(attacked_piece)
                    heappush(actions, (prio, move))

        if len(actions) == 0:
            return None

        return heappop(actions)[1]
