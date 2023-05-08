from typing import Dict, Type

from chess.piece.bishop import Bishop
from chess.piece.king import King
from chess.piece.knight import Knight
from chess.piece.pawn import Pawn
from chess.piece.piece import Piece
from chess.piece.queen import Queen
from chess.piece.rook import Rook

CHAR_TO_PIECE_CLASS: Dict[str, Type[Piece]] = {"p": Pawn, "n": Knight, "b": Bishop, "r": Rook, "q": Queen, "k": King}
