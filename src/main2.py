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

def get_coordinates(model: str) -> Optional[Coordinates]:
    if model.casefold() == "pixel3".casefold():
        return CoordinatesPixel3()
    if model.casefold() == "pixel4".casefold():
        return CoordinatesPixel4()
    if model.casefold() == "mi8lite".casefold():
        return CoordinatesMi8Lite()
    return None


def get_engine(engine: str) -> Optional[ChessEngine]:
    if engine.casefold() == "python_chess".casefold():
        return PythonChessEngine()
    if engine.casefold() == "stockshark".casefold():
        return StocksharkEngine()
    return None


def get_agent(agent: str) -> Optional[Agent]:
    if agent.casefold() == "human".casefold():
        return AgentHuman()
    if agent.casefold() == "random".casefold():
        return AgentRandom()
    if agent.casefold() == "reactive".casefold():
        return AgentReactive()
    if agent.casefold() == "minmax".casefold():
        return AgentMinMaxAB()
    return None


def get_paw_response(play_as_whites: str) -> Optional[bool]:
    if play_as_whites is None:
        return None
    return play_as_whites.casefold() == "y".casefold() or play_as_whites.casefold() == "yes".casefold() or \
        play_as_whites.casefold() == "s".casefold() or play_as_whites.casefold() == "sim".casefold() or \
        play_as_whites.casefold() == "true".casefold()


main_parser = argparse.ArgumentParser(prog="main")
main_parser.add_argument('--model', type=str, required=True, help='Which smartphone model the ADB connects to')
main_parser.add_argument('--engine', type=str, required=True, help='Which chess engine to use')
main_parser.add_argument('--agent', type=str, required=True, help="Which agent model to run on the simulation")

nav_subparser = main_parser.add_subparsers(dest="navigation_mode", required=True,
                                           help="Specifies if the app navigation throught the menus to start a game is "
                                                "automated by the StockShark or if the user has to navigate manually")

menu_nav_manual_parser = nav_subparser.add_parser('menu_nav_manual')
menu_nav_automatic_parser = nav_subparser.add_parser('menu_nav_automatic')

opponent_type_subparser = menu_nav_automatic_parser.add_subparsers(
    dest='opponent_type', required=True,
    help="Insert 'friend' to play against another friend or 'computer' to play against a computer")

vs_friend_parser = opponent_type_subparser.add_parser('vs_friend')
vs_friend_parser.add_argument("--username", type=str, required=True)
vs_friend_parser.add_argument("--play_as_whites", type=str, required=False)
vs_friend_parser.add_argument("--duration", type=int, required=False)

vs_computer_parser = opponent_type_subparser.add_parser('vs_computer')
vs_computer_parser.add_argument("--diff_lvl", type=int, required=True)
vs_computer_parser.add_argument("--play_as_whites", type=str, required=False)

main_args = main_parser.parse_args()

coordinates = get_coordinates(main_args.model)
if coordinates is None:
    raise ValueError("The model is not available to playtest")

engine = get_engine(main_args.engine)
if engine is None:
    raise ValueError("The engine is not recognized")

agent = get_agent(main_args.agent)
if agent is None:
    raise ValueError("The agent type is not recognized")

print("--- Starting STOCKSHARK ---")
stockshark = StockSharkRunnable(coordinates)

nav_automatic = main_args.navigation_mode.casefold() == "menu_nav_automatic"
if nav_automatic:
    stockshark.open_app(5)
    print("Opening app")

    nav_args = menu_nav_automatic_parser.parse_args()

    vs_bot = nav_args.navigation_mode.casefold() == "vs_computer"
    if vs_bot:
        bot_args = vs_computer_parser.parse_args()
        diff_lvl = bot_args.diff_lvl
        on_white_side = get_paw_response(bot_args.play_as_whites)
        print("Starting a game against the computer")
        stockshark.start_game_computer(diff_lvl, on_white_side, 3)
    else:
        friend_args = vs_friend_parser.parse_args()
        username = friend_args.username
        on_white_side = get_paw_response(friend_args.play_as_whites)
        duration = friend_args.duration
        print("Starting a game against a friend")
        stockshark.start_game_friend(username, on_white_side, duration, 3)

print("Playing the game")
stockshark.run_game(agent)
