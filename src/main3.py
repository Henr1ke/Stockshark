import argparse
from typing import Optional

from stockshark.adb.coordinates.coordinates import Coordinates
from stockshark.adb.coordinates.coordinates_mi_8_lite import CoordinatesMi8Lite
from stockshark.adb.coordinates.coordinates_pixel_3 import CoordinatesPixel3
from stockshark.adb.coordinates.coordinates_pixel_4 import CoordinatesPixel4
from stockshark.agent.agent import Agent
from stockshark.agent.agent_human import AgentHuman
from stockshark.agent.agent_min_max_ab import AgentMinMaxAB
from stockshark.agent.agent_random import AgentRandom
from stockshark.agent.agent_reactive import AgentReactive
from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.chess_engine.python_chess_engine import PythonChessEngine
from stockshark.chess_engine.stockshark_engine import StocksharkEngine
from stockshark.run.stockshark_runnable import StockSharkRunnable


# adb start-server
# emulator -avd Pixel_4_API_33 -port 5556

# python main2.py --model pixel4 --engine python_chess --agent minmax menu_nav_automatic vs_friend --username Henrike01
# python main2.py --model pixel4 --engine python_chess --agent minmax menu_nav_automatic vs_computer --diff_lvl 1
# python main2.py --model pixel4 --engine python_chess --agent minmax menu_nav_manual

models_dict = {"pixel4": CoordinatesPixel4, "pixel3": CoordinatesPixel3, "mi8lite": CoordinatesMi8Lite}
engines_dict = {"python_chess": PythonChessEngine, "stockshark": StocksharkEngine()}
agents_dict = {"human": AgentHuman, "random": AgentRandom, "reactive": AgentReactive, "minmax": AgentMinMaxAB}



main_parser = argparse.ArgumentParser(prog="stockshark",
                                      description="StockShark is a chess engine that plays chess on the chess.com app "
                                                  "using ADB to control the smartphone. It can play against a human "
                                                  "friend or against the chess.com computer. The chess.com app "
                                                  "navigation throught the menus to start a game can be automated or "
                                                  "the user can navigate manually.")

main_parser.add_argument('--model', choices=models_dict.keys(), required=True, help='Which smartphone model the ADB connects to')
main_parser.add_argument('--engine', choices=engines_dict.keys(), required=True, help='Which chess engine to use')
main_parser.add_argument('--agent', choices=agents_dict.keys(), required=True, help="Which agent to run on the simulation")

args = main_parser.parse_args()

print(args)