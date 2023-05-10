from chess.player.player import Player
from chess.sim.game import Game
from chess.util.move import Move


class PlayerADB(Player):

    def __init__(self, adb):
        self.adb = adb
        self.is_white: bool = self.adb.is_opponent_white()


    def gen_move(self, game: Game) -> Move:
        if game.last_move is not None:
            self.adb.jogar_online(game.last_move)
        return self.adb.obter_move()
