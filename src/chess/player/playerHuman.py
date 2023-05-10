from chess.player.player import Player
from chess.sim.game import Game
from chess.util.move import Move
from chess.util.position import Position
from chessEngine.chess_components import Simulator


class PlayerHuman(Player):

    @staticmethod
    def get_start_pos(game) -> Position:
        # TODO
        pass

    @staticmethod
    def get_end_pos(game, start_pos: Position) -> Position:
        # TODO
        pass

    def gen_move(self, game) -> Move:
        start_pos = PlayerHuman.get_start_pos(game)
        end_pos = PlayerHuman.get_end_pos(game, start_pos)
        return Move(start_pos, end_pos)
