from stockshark.agent.behaviour.random_behaviour import RandomBehaviour

from stockshark.agent.agent import Agent
from stockshark.chess_engine.game_engine import GameEngine
from stockshark.util.move import Move


class AgentRandom(Agent):
    def __init__(self):
        self.__behaviour = RandomBehaviour()

    def gen_move(self, game: GameEngine) -> Move:
        return self.__behaviour.gen_move(game)
