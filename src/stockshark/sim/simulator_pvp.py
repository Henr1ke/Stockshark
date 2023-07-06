from abc import ABC
from typing import Optional

from stockshark.chess_engine.game_engine import GameEngine

from stockshark.agent.agent import Agent
from stockshark.agent.agent_random import AgentRandom
from stockshark.chess_engine.stockshark_engine import StocksharkEngine
from stockshark.sim.simulator import Simulator
from stockshark.sim.visualizer import Visualizer


class SimulatorPVP(Simulator, ABC):
    def __init__(self, agent_w: Agent, agent_b: Agent, game: GameEngine, vis: Optional[Visualizer]) -> None:
        super().__init__(game, vis)
        self._agent_w: Agent = agent_w
        self._agent_b: Agent = agent_b

    def _update_game(self) -> bool:
        agent = self._agent_w if self._game.is_white_turn else self._agent_b
        move = agent.gen_move(self._game)
        self._game.make_move(move)
        return True


if __name__ == '__main__':
    game = StocksharkEngine()
    agent_w = AgentRandom()
    agent_b = AgentRandom()
    visualizer = Visualizer(Visualizer.CHARSET_LETTER)

    simulator = SimulatorPVP(agent_w, agent_b, game, visualizer)
    simulator.execute()
