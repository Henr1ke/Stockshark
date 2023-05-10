from chess.player.playerADB import PlayerADB
from chess.sim.game import Game, Simulator
from chessEngine.players.player_random import PlayerRandom


# init player adb
adb = start_abd()
player_adb = PlayerADB(adb)
game = Game()

# init other player
player_random = PlayerRandom()

player_w = player_adb if player_adb.is_white else player_random
player_b = player_random if player_adb.is_white else player_adb

simulator = Simulator(game, player_w, player_b)
simulator.execute()