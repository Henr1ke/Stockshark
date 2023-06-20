from typing import Optional

from heapq import heappop, heappush

from stockshark.chess_engine.game import Game
from stockshark.agent.behaviour.behaviour import Behaviour
from stockshark.util.move import Move


class EatBehaviour(Behaviour):

    def gen_move(self, game: Game) -> Optional[Move]:
        actions = []

        pieces_pos = game.get_available_pieces_pos()
        board = game.board

        for piece, start_pos in pieces_pos.items():
            moves = game.get_legal_piece_moves(piece)
            for move in moves:
                attacked_piece = board[move.end_tile]
                if attacked_piece is not None:
                    prio = -attacked_piece.value
                    heappush(actions, (prio, move))

        if len(actions) == 0:
            return None

        return heappop(actions)[1]
