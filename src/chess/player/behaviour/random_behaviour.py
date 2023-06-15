import random
from typing import Optional

from chess.chessGame.chess_game import ChessGame
from chess.player.behaviour.behaviour import Behaviour
from chess.util.move import Move


class RandomBehaviour(Behaviour):

    def gen_move(self, game: ChessGame) -> Optional[Move]:
        pieces_pos = game.get_available_pieces_pos()
        piece = random.choice(list(pieces_pos.keys()))

        moves = game.get_legal_piece_moves(piece)
        move = random.choice(moves)
        return move
