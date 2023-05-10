from chess.player.player import Player
from chess.sim.game import Game
from chess.util.move import Move


class PlayerADB(Player):

    def __init__(self, adb):
        # TODO
        self.adb = adb
        self.is_white: bool = self.adb.is_opponent_white()

    def gen_move(self, game: Game) -> Move:
        moves_played = game.moves_played
        if len(moves_played) > 0:
            self.adb.jogar_online(moves_played[-1])
        return self.adb.obter_move()
