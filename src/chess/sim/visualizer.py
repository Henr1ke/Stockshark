from typing import Dict, Type

from chess.piece.bishop import Bishop
from chess.piece.king import King
from chess.piece.knight import Knight
from chess.piece.pawn import Pawn
from chess.piece.piece import Piece
from chess.piece.queen import Queen
from chess.piece.rook import Rook
from chess.chessGame.state import State
from chess.util.constants import FILE_LETTERS


class Visualizer:
    W_PIECE_CHARSET_LETTER: Dict[Type[Piece], str] = {
        Pawn: "P",
        Knight: "N",
        Bishop: "B",
        Rook: "R",
        Queen: "Q",
        King: "K"
    }
    B_PIECE_CHARSET_LETTER: Dict[Type[Piece], str] = {
        Pawn: "p",
        Knight: "n",
        Bishop: "b",
        Rook: "r",
        Queen: "q",
        King: "k"
    }

    W_PIECE_CHARSET_SYMBOL: Dict[Type[Piece], str] = {
        Pawn: "♟",
        Knight: "♛",
        Bishop: "♜",
        Rook: "♝",
        Queen: "♞",
        King: "♚︎"
    }
    B_PIECE_CHARSET_SYMBOL: Dict[Type[Piece], str] = {
        Pawn: "♙",
        Knight: "♘",
        Bishop: "♗",
        Rook: "♖",
        Queen: "♕",
        King: "♔"
    }

    def __init__(self, w_piece_charset: Dict[Type[Piece], str], b_piece_charset: Dict[Type[Piece], str]) -> None:
        self.__w_piece_charset = w_piece_charset
        self.__b_piece_charset = b_piece_charset

    def show(self, game) -> None:
        print()

        played_moves = game.played_moves
        if len(played_moves) > 0:
            print(f"{'Black' if game.is_white_turn else 'White'} player made the move {played_moves[-1]}")

        if game.state == State.IN_PROGRESS:
            print(f"{'White' if game.is_white_turn else 'Black'} turn to play")
        elif game.state == State.DRAW:
            print(f"Game ended in a draw")
        else:
            winner, loser = ("white", "black") if game.state == State.WIN_W else ("black", "white")
            print(f"Game ended with {winner} player check-mating {loser} player")
        print(f"halfclock: {game.halfclock}, fullclock: {game.fullclock}")
        self.print_board(game.board)

    def print_board(self, board) -> None:
        print("═══╦══" + "═╤══" * (8 - 1) + "═╗")

        for row in range(8 - 1, -1, -1):
            print(f" {row + 1} ║ " + " │ ".join(
                ("·" if (row + col) % 2 == 0 else " ") if board[col, row] is None else self.get_char(board[col, row])
                for col in range(8)
            ) + " ║")

        print(f"═══╬══{'═╪══' * (8 - 1)}═╣")
        print(f"   ║ {' │ '.join(FILE_LETTERS)} ║")

    def get_char(self, piece) -> str:
        piece_charset = self.__w_piece_charset if piece.plays_as_whites else self.__b_piece_charset
        return piece_charset[piece.__class__]
