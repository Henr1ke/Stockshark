import random

from chess.player.player import Player
from chess.chessGame.chessGame import ChessGame
from chess.util.move import Move


class PlayerRandom(Player):

    def gen_move(self, game: ChessGame) -> Move:
        pieces_pos = self.get_available_pieces_pos(game)
        piece, start_pos = random.choice(list(pieces_pos.items()))

        piece_pos = game.get_legal_piece_pos(piece)
        end_pos = random.choice(piece_pos)

        return Move(start_pos, end_pos)
