from typing import Optional

import numpy as np
from stockshark.chess_engine.game_engine import GameEngine

from stockshark.adb.dao_adb import DaoADB
from stockshark.adb.mobile_player import MobilePlayer
from stockshark.agent.agent import Agent
from stockshark.agent.agent_random import AgentRandom
from stockshark.art_vis.detector import Detector
from stockshark.chess_engine.stockshark_engine import StocksharkEngine
from stockshark.sim.simulator import Simulator
from stockshark.sim.visualizer import Visualizer


class SimulatorADB(Simulator):
    def __init__(self, agent: Agent, mobile: MobilePlayer, game: GameEngine, vis: Optional[Visualizer]) -> None:
        super().__init__(game, vis)
        self._agent: Agent = agent
        self._mobile: MobilePlayer = mobile
        self._on_white_side: bool = mobile.on_white_side

    def _update_game(self) -> bool:
        if self._game.is_white_turn == self._on_white_side:
            move = self._agent.gen_move(self._game)
            success = self._game.make_move(move)
            if success:
                self._mobile.play(move)

        else:
            move = self._mobile.get_adv_move(self._game)
            if move is None:
                return False

            self._game.make_move(move)

        return True


if __name__ == '__main__':
    d = DaoADB()
    d.connect()

    screenshot = d.screenshot()
    board_info = Detector.find_board(screenshot)
    if board_info is None:
        exit()

    board, center = board_info

    m = MobilePlayer(d, board, center)

    g = StocksharkEngine()

    v = Visualizer(Visualizer.CHARSET_LETTER)

    agent = AgentRandom()

    simulator = SimulatorADB(agent, m, g, v)
    simulator.execute()

    print(f"{len(agent.TIMES)}")
    print(f"{np.average(agent.TIMES):.4}")
