from abc import ABC, abstractmethod
from typing import Dict

from chess.piece.piece import Piece
from chess.sim.game import Game
from chess.util.move import Move
from chess.util.position import Position


class Player(ABC):
    @staticmethod
    def get_available_pieces_pos(game: Game) -> Dict[Piece, Position]:
        return {piece: pos for piece, pos in game.board.pieces_pos.items()
                if piece.is_white is game.is_white_turn and len(game.get_legal_piece_pos(piece)) > 0}

    @abstractmethod
    def gen_move(self, game: Game) -> Move:
        pass
