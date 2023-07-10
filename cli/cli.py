import argparse
import os
import sys
import time
from typing import Tuple, Optional

from numpy import ndarray

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(src_path)

from stockshark.adb.dao_adb import DaoADB
from stockshark.adb.menu_navigator import MenuNavigator
from stockshark.adb.mobile_player import MobilePlayer
from stockshark.art_vis.detector import Detector
from stockshark.sim.simulator_adb import SimulatorADB
from stockshark.sim.visualizer import Visualizer
from stockshark.adb.coordinates.coordinates_mi_8_lite import CoordinatesMi8Lite
from stockshark.adb.coordinates.coordinates_pixel_3 import CoordinatesPixel3
from stockshark.adb.coordinates.coordinates_pixel_4 import CoordinatesPixel4
from stockshark.agent.agent_human import AgentHuman
from stockshark.agent.agent_min_max_ab import AgentMinMaxAB
from stockshark.agent.agent_random import AgentRandom
from stockshark.agent.agent_reactive import AgentReactive
from stockshark.chess_engine.python_chess_engine import PythonChessEngine
from stockshark.chess_engine.stockshark_engine import StocksharkEngine

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(src_path)


class CLI:
    models_dict = {"pixel4": CoordinatesPixel4, "pixel3": CoordinatesPixel3, "mi8lite": CoordinatesMi8Lite}
    engines_dict = {"python_chess": PythonChessEngine, "stockshark": StocksharkEngine()}
    agents_dict = {"human": AgentHuman, "random": AgentRandom, "reactive": AgentReactive, "minmax": AgentMinMaxAB}
    navigate_menus = "navigate_menus"
    vs_friend = "vs_friend"
    vs_computer = "vs_computer"

    main_parser = argparse.ArgumentParser(
        description="StockShark is a chess engine that plays chess on the chess.com app "
                    "using ADB to control the smartphone. It can play against a human "
                    "friend or against the chess.com computer. The chess.com app "
                    "navigation throught the menus to start a game can be automated or "
                    "the user can navigate manually.")

    main_parser.add_argument('--engine', choices=engines_dict.keys(), required=True, help='Which chess engine to use')
    main_parser.add_argument('--agent', choices=agents_dict.keys(), required=True,
                             help="Which agent to run on the simulation")
    main_parser.add_argument('--show_simulation', action='store_true', required=False,
                             help='If indicated, the internal game simulation is shown on the console')

    nav_mode_subparsers = main_parser.add_subparsers(dest='menu_navigation_mode', required=False)

    navigate_menus_parser = nav_mode_subparsers.add_parser(navigate_menus,
                                                           help='If indicated, the program automatically navigates throught'
                                                                ' chess.com menus to start a game and then plays the game')

    navigate_menus_parser.add_argument('--model', choices=models_dict.keys(), required=True,
                                       help='Which smartphone model the ADB connects to')

    opponent_type_subparsers = navigate_menus_parser.add_subparsers(dest='opponent_type', required=True)

    vs_friend_parser = opponent_type_subparsers.add_parser(vs_friend, help='Play against a human friend')
    vs_friend_parser.add_argument('--username', required=True, help='The username of the friend')
    vs_firend_color_group = vs_friend_parser.add_mutually_exclusive_group(required=False)
    vs_firend_color_group.add_argument('--play_as_whites', action='store_true', help='Play with the white pieces')
    vs_firend_color_group.add_argument('--play_as_blacks', action='store_true', help='Play with the black pieces')
    vs_friend_parser.add_argument('--timers_duration', choices=["1", "3", "5", "10", "30"], default="10",
                                  help='The timers duration, in minutes, that each player has to act during the whole match')

    vs_computer_parser = opponent_type_subparsers.add_parser(vs_computer, help='Play against the chess.com computer')
    vs_computer_parser.add_argument('--diff_lvl', choices=["1", "2", "3", "4", "5"], required=True,
                                    help='The difficulty level of the chess.com coputer')

    vs_computer_color_group = vs_computer_parser.add_mutually_exclusive_group(required=False)
    vs_computer_color_group.add_argument('--play_as_whites', action='store_true', help='Play with the white pieces')
    vs_computer_color_group.add_argument('--play_as_blacks', action='store_true', help='Play with the black pieces')

    args = main_parser.parse_args()

    dao_adb = DaoADB()
    dao_adb.connect()
    if not dao_adb.is_connected:
        print("Error connecting to device, exiting...")
        exit()

    def _app_navigate_menus(self, args, dao_adb) -> None:
        coordinates = CLI.models_dict[args.model]()
        menu_navigator = MenuNavigator(dao_adb, coordinates)

        print("Opening chess.com app...")
        menu_navigator.open_app()

        opponent_type = args.opponent_type
        if opponent_type is not None:
            if opponent_type.casefold() == CLI.vs_friend:
                self._navigate_vs_friend(args, menu_navigator)
            elif opponent_type.casefold() == CLI.vs_computer:
                self._navigate_vs_computer(args, menu_navigator)

    @staticmethod
    def _navigate_vs_friend(args, menu_navigator: MenuNavigator) -> None:
        username = args.username
        play_as_whites = True if args.play_as_whites else False if args.play_as_blacks else None
        timers_duration = int(args.timers_duration)

        print("Navigating through the menus to start a game against a friend...")
        menu_navigator.vs_friend(username, play_as_whites, timers_duration)

    @staticmethod
    def _navigate_vs_computer(args, menu_navigator: MenuNavigator) -> None:
        diff_lvl = int(args.diff_lvl)
        play_as_whites = True if args.play_as_whites else False if args.play_as_blacks else None

        print("Navigating through the menus to start a game against the computer...")
        menu_navigator.vs_computer(diff_lvl, play_as_whites)

    @staticmethod
    def _find_board_info(dao_adb) -> Optional[Tuple[ndarray, Tuple[int, int]]]:
        for _ in range(120):
            screenshot = dao_adb.screenshot()
            board_info = Detector.find_board(screenshot)
            if board_info is None:
                time.sleep(1)
            else:
                return board_info

        return None

    @staticmethod
    def _play_game(args, board_info, dao_adb, engine, agent) -> None:
        board, center = board_info
        mobile_player = MobilePlayer(dao_adb, board, center)
        vis = None if not args.show_simulation else Visualizer(Visualizer.CHARSET_LETTER)
        simulator = SimulatorADB(agent, mobile_player, engine, vis)

        print("Starting the game simulation...")
        simulator.execute()
        print("Game ended, exiting the script...")

    def run(self) -> None:
        main_parser = argparse.ArgumentParser(
            description="StockShark is a chess engine that plays chess on the chess.com app "
                        "using ADB to control the smartphone. It can play against a human "
                        "friend or against the chess.com computer. The chess.com app "
                        "navigation throught the menus to start a game can be automated or "
                        "the user can navigate manually.")

        main_parser.add_argument('--engine', choices=CLI.engines_dict.keys(), required=True,
                                 help='Which chess engine to use')
        main_parser.add_argument('--agent', choices=CLI.agents_dict.keys(), required=True,
                                 help="Which agent to run on the simulation")
        main_parser.add_argument('--show_simulation', action='store_true', required=False,
                                 help='If indicated, the internal game simulation is shown on the console')

        nav_mode_subparsers = main_parser.add_subparsers(dest='menu_navigation_mode', required=False)

        navigate_menus_parser = nav_mode_subparsers.add_parser(CLI.navigate_menus,
                                                               help='If indicated, the program automatically navigates throught'
                                                                    ' chess.com menus to start a game and then plays the game')

        navigate_menus_parser.add_argument('--model', choices=CLI.models_dict.keys(), required=True,
                                           help='Which smartphone model the ADB connects to')

        opponent_type_subparsers = navigate_menus_parser.add_subparsers(dest='opponent_type', required=True)

        vs_friend_parser = opponent_type_subparsers.add_parser(CLI.vs_friend, help='Play against a human friend')
        vs_friend_parser.add_argument('--username', required=True, help='The username of the friend')
        vs_firend_color_group = vs_friend_parser.add_mutually_exclusive_group(required=False)
        vs_firend_color_group.add_argument('--play_as_whites', action='store_true', help='Play with the white pieces')
        vs_firend_color_group.add_argument('--play_as_blacks', action='store_true', help='Play with the black pieces')
        vs_friend_parser.add_argument('--timers_duration', choices=["1", "3", "5", "10", "30"], default="10",
                                      help='The timers duration, in minutes, that each player has to act during the whole match')

        vs_computer_parser = opponent_type_subparsers.add_parser(CLI.vs_computer,
                                                                 help='Play against the chess.com computer')
        vs_computer_parser.add_argument('--diff_lvl', choices=["1", "2", "3", "4", "5"], required=True,
                                        help='The difficulty level of the chess.com coputer')

        vs_computer_color_group = vs_computer_parser.add_mutually_exclusive_group(required=False)
        vs_computer_color_group.add_argument('--play_as_whites', action='store_true', help='Play with the white pieces')
        vs_computer_color_group.add_argument('--play_as_blacks', action='store_true', help='Play with the black pieces')

        args = main_parser.parse_args()

        dao_adb = DaoADB()
        dao_adb.connect()
        if not dao_adb.is_connected:
            print("Error connecting to device, exiting...")
            exit()

        print()
        print(args)
        print()
        print("--- Starting STOCKSHARK ---")

        engine = CLI.engines_dict[args.engine]()
        agent = CLI.agents_dict[args.agent]()

        menu_navigation_mode = args.menu_navigation_mode
        if menu_navigation_mode is not None and menu_navigation_mode.casefold() == CLI.navigate_menus:
            self._app_navigate_menus(args, dao_adb)

        print("Searching for the board on the screen...")
        board_info = self._find_board_info(dao_adb)

        if board_info is None:
            print("The waiting time was exceeded, exiting aplication")
            exit()
        else:
            print("The board was found on the screen")
            self._play_game(args, board_info, dao_adb, engine, agent)


cli = CLI()
cli.run()
