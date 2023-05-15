from chess.chessGame.chessGame import ChessGame
from chess.player.playerRandom import PlayerRandom
from chess.sim.simulatorPVP import SimulatorPVP
from chess.sim.visualizer import Visualizer

game = ChessGame()
player_w = PlayerRandom()
player_b = PlayerRandom()
visualizer = Visualizer(Visualizer.W_PIECE_CHARSET_LETTER, Visualizer.B_PIECE_CHARSET_LETTER)

simulator = SimulatorPVP(player_w, player_b, game, visualizer)
simulator.execute()
