import argparse
from typing import Optional

from chess.adb.coordinates.coordinates import Coordinates
from chess.adb.coordinates.coordinatesMi8Lite import CoordinatesMi8Lite
from chess.adb.coordinates.coordinatesPixel4 import CoordinatesPixel4
from chess.adb.daoADB import DaoADB
from chess.adb.menuNavigator import MenuNavigator
from chess.adb.mobileChess import MobileChess
from chess.chessGame.chessGame import ChessGame
from chess.player.playerRandom import PlayerRandom
from chess.sim.simulatorADB import SimulatorADB
from chess.sim.visualizer import Visualizer


def get_coordinates(phone_model: str) -> Optional[Coordinates]:
    if phone_model.casefold() == "pixel4".casefold():
        return CoordinatesPixel4()
    if phone_model.casefold() == "mi8lite".casefold():
        return CoordinatesMi8Lite()
    return None


parser = argparse.ArgumentParser()
parser.add_argument('--phone_model', type=str, required=True, help='Which smartphone model the ADB connects to')
subparser = parser.add_subparsers(dest='opponent_type', required=True,
                                  help="Insert 'player' to play against another player or 'computer' to play against a computer")

player = subparser.add_parser('player')
player.add_argument("--username", type=str, required=True)
player.add_argument("--play_as_whites", type=bool, required=False)
player.add_argument("--duration", type=int, required=False)

computer = subparser.add_parser('computer')
computer.add_argument("--diff_lvl", type=int, required=True)
computer.add_argument("--play_as_whites", type=bool, required=False)

args = parser.parse_args()
print("entrou")
print(args)

coordinates = get_coordinates(args.phone_model)
if coordinates is None:
    raise ValueError("The model is not available to playtest")

dao_adb = DaoADB()
connected = dao_adb.connect()
if not connected:
    raise RuntimeError("Error connecting to the device")

menu_navigator = MenuNavigator(dao_adb, coordinates)
menu_navigator.open_app()

vs_bot = args.opponent_type.casefold() == "computer"
if vs_bot:
    diff_lvl = args.diff_lvl
    is_white = args.play_as_whites
    menu_navigator.vs_bot(diff_lvl, is_white)

else:
    name = args.username
    is_white = args.play_as_whites
    duration = args.duration
    menu_navigator.vs_player(name, is_white, duration)

mobile_chess = MobileChess(dao_adb, coordinates, vs_bot)

g = ChessGame()

v = Visualizer(Visualizer.W_PIECE_CHARSET_LETTER, Visualizer.B_PIECE_CHARSET_LETTER)

simulator = SimulatorADB(PlayerRandom(), mobile_chess, g, v)
simulator.execute()
