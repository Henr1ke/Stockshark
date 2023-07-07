import random
from typing import Optional

from stockshark.agent.behaviour.behaviour import Behaviour
from stockshark.chess_engine.chess_engine import ChessEngine


class RandomBehaviour(Behaviour):

    def gen_move(self, engine: ChessEngine) -> Optional[str]:
        moves = engine.available_moves
        move = random.choice(moves)
        return move
