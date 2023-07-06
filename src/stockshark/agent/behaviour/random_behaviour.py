import random
from typing import Optional

from stockshark.chess_engine.game_engine import GameEngine

from stockshark.agent.behaviour.behaviour import Behaviour
from stockshark.util.move import Move


class RandomBehaviour(Behaviour):

    def gen_move(self, game: GameEngine) -> Optional[Move]:
        pieces_tile = game.get_available_pieces_tiles()
        piece = random.choice(list(pieces_tile.keys()))

        moves = game.get_legal_piece_moves(piece)
        move = random.choice(moves)
        return move
