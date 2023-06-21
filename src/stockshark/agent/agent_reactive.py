from typing import List, Optional

from stockshark.agent.agent import Agent
from stockshark.agent.behaviour.behaviour import Behaviour
from stockshark.agent.behaviour.eat_behaviour import EatBehaviour
from stockshark.agent.behaviour.random_behaviour import RandomBehaviour
from stockshark.chess_engine.game_engine import GameEngine
from stockshark.util.move import Move


class AgentReactive(Agent):
    def __init__(self, behaviours: Optional[List[Behaviour]] = None):
        if behaviours is None:
            behaviours = [EatBehaviour(), RandomBehaviour()]
        if len(behaviours) < 2:
            raise ValueError("A reactive agent must have 2 or more behaviours")
        self.__behaviours = behaviours
        self.__random_behaviour = RandomBehaviour()

    def gen_move(self, game: GameEngine) -> Move:
        for behaviour in self.__behaviours:
            move = behaviour.gen_move(game)
            if move is not None:
                return move

        return self.__random_behaviour.gen_move(game)
