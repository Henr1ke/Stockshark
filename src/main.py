import argparse
from typing import Optional

from chess.adb.coordinates.coordinates import Coordinates
from chess.adb.coordinates.coordinates_mi_8_lite import CoordinatesMi8Lite
from chess.adb.coordinates.coordinates_pixel_4 import CoordinatesPixel4
from chess.adb.dao_adb import DaoADB
from chess.adb.menu_navigator import MenuNavigator
from chess.adb.mobile_chess import MobileChess
from chess.chessGame.chess_game import ChessGame
from chess.player.player import Player
from chess.player.player_human import PlayerHuman
from chess.player.player_random import PlayerRandom
from chess.player.player_reactive import PlayerReactive
from chess.sim.simulator_adb import SimulatorADB
from chess.sim.visualizer import Visualizer


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
print("\n--- A INICIAR STOCKSHARK ---\n")

player = get_player(args.player)
if player is None:
    raise ValueError("The player type is not recognized")

coordinates = get_coordinates(args.model)
if coordinates is None:
    raise ValueError("The model is not available to playtest")

dao_adb = DaoADB()
connected = dao_adb.connect()
if not connected:
    raise RuntimeError("Error connecting to the device")

print("A abrir aplicação\n")

menu_navigator = MenuNavigator(dao_adb, coordinates)
menu_navigator.open_app()
print("A selecionar o adversário\n")

vs_bot = args.opponent_type.casefold() == "computer"
if vs_bot:
    diff_lvl = args.diff_lvl
    is_white = get_paw_response(args.play_as_whites)
    menu_navigator.vs_computer(diff_lvl, is_white)

else:
    name = args.username
    is_white = get_paw_response(args.play_as_whites)
    duration = args.duration
    menu_navigator.vs_player(name, is_white, duration)

input("Pressiona Enter assim que o jogo estiver pronto para iniciar a simulação\n")
print("A iniciar simulação\n")
mobile_chess = MobileChess(dao_adb, coordinates, vs_bot)

game = ChessGame()
vis = Visualizer(Visualizer.W_PIECE_CHARSET_LETTER, Visualizer.B_PIECE_CHARSET_LETTER)

simulator = SimulatorADB(player, mobile_chess, game, vis)
simulator.execute()
