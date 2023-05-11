from chess.player.playerRandom import PlayerRandom
from chess.sim.game import Game
from chess.sim.simulator import Simulator
from chess.sim.visualizer import Visualizer

# # init player adb
# adb = start_abd()
# player_adb = PlayerADB(adb)
# game = Game()
#
# # init other player
# player_random = PlayerRandom()
#
# player_w = player_adb if player_adb.is_white else player_random
# player_b = player_random if player_adb.is_white else player_adb
#
# simulator = Simulator(game, player_w, player_b)
# simulator.execute()

simulator = Simulator(Game(), PlayerRandom(), PlayerRandom(), Visualizer(Visualizer.PIECE_TO_LETTER))
simulator.execute()
