import argparse

from stockshark.adb.coordinates.coordinates_mi_8_lite import CoordinatesMi8Lite
from stockshark.adb.coordinates.coordinates_pixel_3 import CoordinatesPixel3
from stockshark.adb.coordinates.coordinates_pixel_4 import CoordinatesPixel4
from stockshark.agent.agent_human import AgentHuman
from stockshark.agent.agent_min_max_ab import AgentMinMaxAB
from stockshark.agent.agent_random import AgentRandom
from stockshark.agent.agent_reactive import AgentReactive
from stockshark.chess_engine.python_chess_engine import PythonChessEngine
from stockshark.chess_engine.stockshark_engine import StocksharkEngine

# adb start-server
# emulator -avd Pixel_4_API_33 -port 5556

# python main2.py --model pixel4 --engine python_chess --agent minmax menu_nav_automatic vs_friend --username Henrike01
# python main2.py --model pixel4 --engine python_chess --agent minmax menu_nav_automatic vs_computer --diff_lvl 1
# python main2.py --model pixel4 --engine python_chess --agent minmax menu_nav_manual


models_dict = {"pixel4": CoordinatesPixel4, "pixel3": CoordinatesPixel3, "mi8lite": CoordinatesMi8Lite}
engines_dict = {"python_chess": PythonChessEngine, "stockshark": StocksharkEngine()}
agents_dict = {"human": AgentHuman, "random": AgentRandom, "reactive": AgentReactive, "minmax": AgentMinMaxAB}

main_parser = argparse.ArgumentParser(description="StockShark is a chess engine that plays chess on the chess.com app "
                                                  "using ADB to control the smartphone. It can play against a human "
                                                  "friend or against the chess.com computer. The chess.com app "
                                                  "navigation throught the menus to start a game can be automated or "
                                                  "the user can navigate manually.")

main_parser.add_argument('--model', choices=models_dict.keys(), required=True,
                         help='Which smartphone model the ADB connects to')
main_parser.add_argument('--engine', choices=engines_dict.keys(), required=True, help='Which chess engine to use')
main_parser.add_argument('--agent', choices=agents_dict.keys(), required=True,
                         help="Which agent to run on the simulation")

nav_mode_subparsers = main_parser.add_subparsers(dest='menu_navigation_mode', required=True)

menu_nav_manual_parser = nav_mode_subparsers.add_parser('menu_nav_manual',
                                                        help='The program assumes that the user has already '
                                                             'navigated throught chess.com menus to start a '
                                                             'game and it will only play the game')
menu_nav_automatic_parser = nav_mode_subparsers.add_parser('menu_nav_automatic',
                                                           help='The program automatically navigates '
                                                                'throught chess.com menus to start a game '
                                                                'and then plays the game')

opponent_type_subparsers = menu_nav_automatic_parser.add_subparsers(dest='oppenent_type', required=True)

vs_friend_parser = opponent_type_subparsers.add_parser('vs_friend', help='Play against a human friend')
vs_friend_parser.add_argument('--username', required=True, help='The username of the friend')
vs_firend_color_group = vs_friend_parser.add_mutually_exclusive_group(required=False)
vs_firend_color_group.add_argument('--play_as_whites', action='store_true', help='Play with the white pieces')
vs_firend_color_group.add_argument('--play_as_blacks', action='store_true', help='Play with the black pieces')
vs_friend_parser.add_argument('--player_timers', choices=[1, 3, 5, 10, 30], default=10, help='The timer duration, in '
                                                                                             'minutes, that each '
                                                                                             'player has to act during '
                                                                                             'the whole match')

vs_computer_parser = opponent_type_subparsers.add_parser('vs_computer', help='Play against the chess.com computer')
vs_computer_parser.add_argument('--diff_lvl', choices=[1, 2, 3, 4, 5], default=1, help='The difficulty level of the '
                                                                                       'chess.com coputer')
vs_computer_color_group = vs_computer_parser.add_mutually_exclusive_group(required=False)
vs_computer_color_group.add_argument('--play_as_whites', action='store_true', help='Play with the white pieces')
vs_computer_color_group.add_argument('--play_as_blacks', action='store_true', help='Play with the black pieces')

args = main_parser.parse_args()

print(args)
