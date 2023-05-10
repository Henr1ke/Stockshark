from chess.sim.game import Game
from chess.util.move import Move


class GameRules:
    @staticmethod
    def is_legal_move(game: Game, move: Move) -> bool:
        pass

    @staticmethod
    def king_is_under_atk(game: Game, is_white: bool) -> bool:
        pass

    @staticmethod
    def leaves_king_under_atk(game: Game, move: Move) -> bool:
        pass
