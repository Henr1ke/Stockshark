from copy import copy

from chess.util.move import Move


class GameRules:
    @staticmethod
    def is_legal_move(game, move: Move) -> bool:
        piece = game.board[move.start_pos]
        return piece is not None and piece.is_white is game.is_white_turn and \
            move.end_pos in game.get_legal_piece_pos(piece)

    @staticmethod
    def king_is_under_atk(game) -> bool:
        board = game.board

        king_is_white = not game.is_white_turn

        if king_is_white not in board.kings_pos.keys():
            return False
        king_pos = board.kings_pos[king_is_white]

        atk_pieces_pos = {piece: pos for piece, pos in board.pieces_pos.items() if piece.is_white is not king_is_white}

        for atk_piece, pos in atk_pieces_pos.items():
            if king_pos in atk_piece.gen_positions(game, pos):
                return True
        return False

    @staticmethod
    def leaves_king_under_atk(game, move: Move) -> bool:
        game_copy = copy(game)
        game_copy.play(move, False)
        return GameRules.king_is_under_atk(game_copy)
