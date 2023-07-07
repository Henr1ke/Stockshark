import time

from stockshark.agent.agent import Agent
from stockshark.agent.behaviour.random_behaviour import RandomBehaviour
from stockshark.chess_engine.chess_engine import ChessEngine


class AgentRandom(Agent):
    TIMES = []

    def __init__(self):
        self.__behaviour = RandomBehaviour()

    def gen_move(self, engine: ChessEngine) -> str:
        ti = time.time_ns()
        move = self.__behaviour.gen_move(engine)
        AgentRandom.TIMES.append(time.time_ns() - ti)
        return move
