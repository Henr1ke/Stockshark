from typing import Optional

from stockshark.adb.dao_adb import DaoADB
from stockshark.adb.mobile_player import MobilePlayer
from stockshark.agent.agent import Agent
from stockshark.agent.agent_human import AgentHuman
from stockshark.agent.agent_min_max_ab import AgentMinMaxAB
from stockshark.agent.agent_random import AgentRandom
from stockshark.agent.agent_reactive import AgentReactive
from stockshark.art_vis.detector import Detector
from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.chess_engine.python_chess_engine import PythonChessEngine
from stockshark.sim.simulator import Simulator
from stockshark.sim.visualizer import Visualizer


class SimulatorADB(Simulator):
    def __init__(self, agent: Agent, mobile: MobilePlayer, engine: ChessEngine, vis: Optional[Visualizer]) -> None:
        super().__init__(engine, vis)
        self._agent: Agent = agent
        self._mobile: MobilePlayer = mobile
        self._on_white_side: bool = mobile.on_white_side

    def _update_game(self) -> bool:
        is_white_turn = self._engine.fen.split()[1] == 'w'
        if is_white_turn == self._on_white_side:
            move = self._agent.gen_move(self._engine)
            success = self._engine.play(move)
            if success:
                self._mobile.play(move)

        else:
            move = self._mobile.get_adv_move(self._engine)
            if move is None:
                return False

            self._engine.play(move)

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

    g = PythonChessEngine()

    v = Visualizer(Visualizer.CHARSET_LETTER)

    # agent = AgentMinMaxAB(4)
    # agent = AgentRandom()
    agent = AgentReactive()
    # agent = AgentHuman()

    simulator = SimulatorADB(agent, m, g, v)
    simulator.execute()

    # print(f"{len(agent.TIMES)}")
    # print(f"{np.average(agent.TIMES):.4}")
