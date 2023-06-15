import random
from typing import Optional

from chess.chessGame.chess_game import ChessGame
from chess.player.behaviour.behaviour import Behaviour
from chess.util.move import Move


class RandomBehaviour(Behaviour):

    def gen_move(self, game: ChessGame) -> Optional[Move]:
        return random.choice(game.legal_moves)
