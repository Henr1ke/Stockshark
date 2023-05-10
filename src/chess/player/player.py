from abc import ABC, abstractmethod
from typing import Dict

from chess.piece.piece import Piece
from chess.sim.game import Game
from chess.util.move import Move
from chess.util.position import Position


class Player(ABC):
    @staticmethod
    def get_available_pieces_pos(game: Game) -> Dict[Piece: Position]:
        pieces_pos = game.board.get_pieces_pos(game.is_white_turn)
        available_pieces_pos = {piece: pos for piece, pos in pieces_pos.items()
                                if len(game.get_positions(piece, pos)) > 0}
        return available_pieces_pos

    @abstractmethod
    def gen_move(self, game: Game) -> Move:
        pass