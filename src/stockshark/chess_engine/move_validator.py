from copy import copy

from stockshark.piece.king import King
from stockshark.util.move import Move


class MoveValidator:

    @staticmethod
    def is_legal(game, move: Move) -> bool:
        king_is_under_atk = MoveValidator.king_is_under_atk(game, game.is_white_turn)
        return not MoveValidator.leaves_king_under_atk(game, move) and \
            (not king_is_under_atk or king_is_under_atk and not MoveValidator.is_castle(game, move))

    @staticmethod
    def king_is_under_atk(game, is_white: bool) -> bool:
        board = game.board

        if is_white not in board.kings.keys():
            return False

        king = board.kings[is_white]
        atk_pieces = [piece for piece in board.pieces_tiles.keys() if piece.is_white is not is_white]

        for atk_piece in atk_pieces:
            moves = atk_piece.gen_moves(game)
            if king in [board[move.end_tile] for move in moves]:
                return True
        return False

    @staticmethod
    def leaves_king_under_atk(game, move: Move) -> bool:
        game_copy = copy(game)
        game_copy.make_move(move, is_test=True)
        return MoveValidator.king_is_under_atk(game_copy, not game_copy.is_white_turn)

    @staticmethod
    def is_castle(game, move: Move) -> bool:
        piece = game.board[move.start_tile]

        if not isinstance(piece, King):
            return False

        if not (move.start_tile.col == 4 and move.start_tile.row == (0 if piece.is_white else 7)):
            return False

        if move.end_tile.col == 1:
            castling_side = "q"
        elif move.end_tile.col == 6:
            castling_side = "k"
        else:
            return False

        castling_side = castling_side.upper() if piece.is_white else castling_side
        if castling_side not in game.castlings:
            return False

        return True
