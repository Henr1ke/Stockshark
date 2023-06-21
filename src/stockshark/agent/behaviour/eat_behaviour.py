from heapq import heappop, heappush
from typing import Optional

from stockshark.agent.behaviour.behaviour import Behaviour
from stockshark.chess_engine.game_engine import GameEngine
from stockshark.util.move import Move


class EatBehaviour(Behaviour):

    def gen_move(self, game: GameEngine) -> Optional[Move]:
        actions = []

        pieces_tile = game.get_available_pieces_tiles()
        board = game.board

        for piece, start_tile in pieces_tile.items():
            moves = game.get_legal_piece_moves(piece)
            for move in moves:
                attacked_piece = board[move.end_tile]
                if attacked_piece is not None:
                    prio = -attacked_piece.value
                    heappush(actions, (prio, move))

        if len(actions) == 0:
            return None

        return heappop(actions)[1]
