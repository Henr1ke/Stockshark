from chess.player.player import Player
from chess.chessGame.chessGame import ChessGame
from chess.util.move import Move


class PlayerADB(Player):

    def __init__(self, adb) -> None:
        # TODO
        self.adb = adb
        self.__is_white: bool = self.adb.is_opponent_white()

    @property
    def is_white(self) -> bool:
        return self.__is_white

    def gen_move(self, game: ChessGame) -> Move:
        played_moves = game.played_moves
        if len(played_moves) > 0:
            self.adb.jogar_online(played_moves[-1])
        return self.adb.obter_move()
