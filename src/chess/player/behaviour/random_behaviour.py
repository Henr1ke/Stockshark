import random
from typing import Optional

from chess.chessGame.chessGame import ChessGame
from chess.player.behaviour.behaviour import Behaviour
from chess.util.move import Move


class RandomBehaviour(Behaviour):

    def gen_move(self, game: ChessGame) -> Optional[Move]:
        pieces_pos = game.get_available_pieces_pos()
        piece, start_pos = random.choice(list(pieces_pos.items()))

        piece_pos = game.get_legal_piece_pos(piece)
        end_pos = random.choice(piece_pos)

        return Move(start_pos, end_pos)
