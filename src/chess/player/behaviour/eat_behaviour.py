import random
from typing import Optional

from heapq import heappop, heappush

from chess.chessGame.chess_game import ChessGame
from chess.piece.bishop import Bishop
from chess.piece.king import King
from chess.piece.knight import Knight
from chess.piece.pawn import Pawn
from chess.piece.piece import Piece
from chess.piece.queen import Queen
from chess.piece.rook import Rook
from chess.player.behaviour.behaviour import Behaviour
from chess.util.move import Move


class EatBehaviour(Behaviour):

    @staticmethod
    def get_prio(piece: Piece):
        if isinstance(piece, Pawn):
            return 1
        if isinstance(piece, Knight):
            return 3
        if isinstance(piece, Bishop):
            return 3
        if isinstance(piece, Rook):
            return 5
        if isinstance(piece, Queen):
            return 9
        if isinstance(piece, King):
            return 50

    def gen_move(self, game: ChessGame) -> Optional[Move]:
        actions = []

        pieces_pos = game.get_available_pieces_pos()
        board = game.board

        for piece, start_pos in pieces_pos.items():
            piece_pos = game.get_legal_piece_pos(piece)
            for end_pos in piece_pos:
                attacked_piece = board[end_pos]
                if attacked_piece is not None:
                    move = Move(start_pos, end_pos)
                    prio = -EatBehaviour.get_prio(attacked_piece)
                    heappush(actions, (prio, move))

        if len(actions) == 0:
            return None

        return heappop(actions)[1]
