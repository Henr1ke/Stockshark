import time

from stockshark.agent.agent import Agent
from stockshark.agent.behaviour.random_behaviour import RandomBehaviour
from stockshark.chess_engine.game_engine import GameEngine
from stockshark.util.move import Move


class AgentRandom(Agent):
    TIMES = []

    def __init__(self):
        self.__behaviour = RandomBehaviour()

    def gen_move(self, game: GameEngine) -> Move:
        ti = time.time_ns()
        move = self.__behaviour.gen_move(game)
        AgentRandom.TIMES.append(time.time_ns() - ti)
        return move
