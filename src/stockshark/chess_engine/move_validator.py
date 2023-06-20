from copy import copy

from stockshark.util.move import Move


class MoveValidator:

    @staticmethod
    def is_legal(game, move: Move) -> bool:
        piece = game.board[move.start_tile]
        return move not in game.get_legal_piece_moves(piece)

    @staticmethod
    def king_is_under_atk(game, is_white: bool) -> bool:
        board = game.board

        if is_white not in board.kings.keys():
            return False

        king = board.kings[is_white]
        atk_pieces = [piece for piece in board.pieces_pos.keys() if piece.is_white is not is_white]

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
