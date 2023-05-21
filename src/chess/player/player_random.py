from chess.player.behaviour.random_behaviour import RandomBehaviour
from chess.player.player import Player
from chess.chessGame.chess_game import ChessGame
from chess.util.move import Move


class PlayerRandom(Player):
    def __init__(self):
        self.__behaviour = RandomBehaviour()

    def gen_move(self, game: ChessGame) -> Move:
        return self.__behaviour.gen_move(game)
