from abc import ABC
from typing import Optional

from stockshark.agent.agent import Agent
from stockshark.agent.agent_human import AgentHuman
from stockshark.agent.agent_min_max import AgentMinMax
from stockshark.agent.agent_min_max_ab import AgentMinMaxAB
from stockshark.agent.agent_random import AgentRandom
from stockshark.agent.agent_reactive import AgentReactive
from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.chess_engine.python_chess_engine import PythonChessEngine
from stockshark.chess_engine.stockshark_engine import StocksharkEngine
from stockshark.sim.simulator import Simulator
from stockshark.sim.visualizer import Visualizer


class SimulatorPVP(Simulator, ABC):
    def __init__(self, agent_w: Agent, agent_b: Agent, engine: ChessEngine, vis: Optional[Visualizer]) -> None:
        super().__init__(engine, vis)
        self._agent_w: Agent = agent_w
        self._agent_b: Agent = agent_b

    def _update_game(self) -> bool:
        is_white_turn = self._engine.fen.split()[1] == 'w'
        agent = self._agent_w if is_white_turn else self._agent_b
        move = agent.gen_move(self._engine)
        self._engine.play(move)
        return True


if __name__ == '__main__':
    engine = StocksharkEngine()
    # engine = PythonChessEngine()
    agent_w = AgentRandom()
    agent_b = AgentMinMaxAB()
    visualizer = Visualizer(Visualizer.CHARSET_LETTER)

    simulator = SimulatorPVP(agent_w, agent_b, engine, visualizer)
    simulator.execute()
