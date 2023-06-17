from typing import List, Optional

from stockshark.chess_engine.game import Game
from stockshark.player.behaviour.behaviour import Behaviour
from stockshark.player.behaviour.eat_behaviour import EatBehaviour
from stockshark.player.behaviour.random_behaviour import RandomBehaviour
from stockshark.player.player import Player
from stockshark.util.move import Move


class PlayerReactive(Player):
    def __init__(self, behaviours: Optional[List[Behaviour]] = None):
        if behaviours is None:
            behaviours = [EatBehaviour(), RandomBehaviour()]
        if len(behaviours) < 2:
            raise ValueError("A reactive player must have 2 or more behaviours")
        self.__behaviours = behaviours
        self.__random_behaviour = RandomBehaviour()

    def gen_move(self, game: Game) -> Move:
        for behaviour in self.__behaviours:
            move = behaviour.gen_move(game)
            if move is not None:
                return move

        return self.__random_behaviour.gen_move(game)
