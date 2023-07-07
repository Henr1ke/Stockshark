from heapq import heappop, heappush
from typing import Optional

from stockshark.agent.behaviour.behaviour import Behaviour
from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.piece.piece import Piece


class EatBehaviour(Behaviour):

    def gen_move(self, engine: ChessEngine) -> Optional[str]:
        actions = []

        moves = engine.available_moves
        for move in moves:
            attacked_tile = move[2:4]
            attacked_piece = engine.get_piece_at(attacked_tile)
            if attacked_piece is not None:
                prio = - Piece.get_piece_value(attacked_piece)
                heappush(actions, (prio, move))

        if len(actions) == 0:
            return None

        return heappop(actions)[1]
