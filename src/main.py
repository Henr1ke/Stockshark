import argparse
import time
from typing import Optional

from stockshark.adb.coordinates.coordinates import Coordinates
from stockshark.adb.coordinates.coordinates_mi_8_lite import CoordinatesMi8Lite
from stockshark.adb.coordinates.coordinates_pixel_4 import CoordinatesPixel4
from stockshark.adb.dao_adb import DaoADB
from stockshark.adb.menu_navigator import MenuNavigator
from stockshark.adb.mobile_chess import MobileChess
from stockshark.art_vis.detector import Detector
from stockshark.chess_engine.game import Game
from stockshark.player.player import Player
from stockshark.player.player_human import PlayerHuman
from stockshark.player.player_min_max import PlayerMinMax
from stockshark.player.player_random import PlayerRandom
from stockshark.player.player_reactive import PlayerReactive
from stockshark.run.stockshark_runnable import StockSharkRunnable
from stockshark.sim.simulator_adb import SimulatorADB
from stockshark.sim.visualizer import Visualizer


# adb start-server
# emulator -avd Pixel_4_API_33 -port 5556

# python main.py --player reactive --model pixel4 friend --username Henrike01
# python main.py --player reactive --model pixel4 computer --diff_lvl 1

def get_coordinates(model: str) -> Optional[Coordinates]:
    if model.casefold() == "pixel4".casefold():
        return CoordinatesPixel4()
    if model.casefold() == "mi8lite".casefold():
        return CoordinatesMi8Lite()
    return None


def get_player(player: str) -> Optional[Player]:
    if player.casefold() == "human".casefold():
        return PlayerHuman()
    if player.casefold() == "random".casefold():
        return PlayerRandom()
    if player.casefold() == "reactive".casefold():
        return PlayerReactive()
    if player.casefold() == "minmax".casefold():
        return PlayerMinMax()
    return None


def get_paw_response(play_as_whites: str) -> Optional[bool]:
    if play_as_whites is None:
        return None
    return play_as_whites.casefold() == "y".casefold() or play_as_whites.casefold() == "yes".casefold() or play_as_whites.casefold() == "s".casefold() or play_as_whites.casefold() == "sim".casefold() or play_as_whites.casefold() == "true".casefold()


parser = argparse.ArgumentParser()
parser.add_argument('--player', type=str, required=True, help="Which player model to run on the simulation")
parser.add_argument('--model', type=str, required=True, help='Which smartphone model the ADB connects to')
subparser = parser.add_subparsers(dest='opponent_type', required=True,
                                  help="Insert 'friend' to play against another friend or 'computer' to play against a computer")

friend = subparser.add_parser('friend')
friend.add_argument("--username", type=str, required=True)
friend.add_argument("--play_as_whites", type=str, required=False)
friend.add_argument("--duration", type=int, required=False)

computer = subparser.add_parser('computer')
computer.add_argument("--diff_lvl", type=int, required=True)
computer.add_argument("--play_as_whites", type=str, required=False)

args = parser.parse_args()

player = get_player(args.player)
if player is None:
    raise ValueError("The player type is not recognized")

coordinates = get_coordinates(args.model)
if coordinates is None:
    raise ValueError("The model is not available to playtest")

player = get_player(args.player)
if player is None:
    raise ValueError("The player type is not recognized")

coordinates = get_coordinates(args.model)
if coordinates is None:
    raise ValueError("The model is not available to playtest")

print("--- Starting STOCKSHARK ---")
stockshark = StockSharkRunnable(coordinates)

stockshark.open_app(8)
print("Opening app")

vs_bot = args.opponent_type.casefold() == "computer"
if vs_bot:
    diff_lvl = args.diff_lvl
    on_white_side = get_paw_response(args.play_as_whites)
    print("Starting a game against the computer")
    stockshark.start_game_computer(diff_lvl, on_white_side, 3)
else:
    username = args.username
    on_white_side = get_paw_response(args.play_as_whites)
    duration = args.duration
    print("Starting a game against a friend")
    stockshark.start_game_friend(username, on_white_side, duration, 3)

print("Playing the game")
stockshark.run_game(player)
