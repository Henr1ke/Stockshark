import random
from typing import Optional

from stockshark.chess_engine.game import Game
from stockshark.agent.behaviour.behaviour import Behaviour
from stockshark.util.move import Move


class RandomBehaviour(Behaviour):

    def gen_move(self, game: Game) -> Optional[Move]:
        pieces_pos = game.get_available_pieces_pos()
        piece = random.choice(list(pieces_pos.keys()))

        moves = game.get_legal_piece_moves(piece)
        move = random.choice(moves)
        return move
