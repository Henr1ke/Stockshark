from copy import copy

from chess.util.move import Move


class ChessRules:
    @staticmethod
    def is_legal_move(game, move: Move) -> bool:
        piece = game.board[move.start_pos]
        return piece is not None and piece.plays_as_whites is game.is_white_turn and \
            move.end_pos in game.get_legal_piece_pos(piece)

    @staticmethod
    def king_is_under_atk(game, is_white) -> bool:
        board = game.board

        if is_white not in board.kings_pos.keys():
            return False
        king_pos = board.kings_pos[is_white]

        atk_pieces_pos = {piece: pos for piece, pos in board.pieces_pos.items() if piece.plays_as_whites is not is_white}

        for atk_piece in atk_pieces_pos.keys():
            if king_pos in atk_piece.gen_positions(game):
                return True
        return False

    @staticmethod
    def leaves_king_under_atk(game, move: Move) -> bool:
        game_copy = copy(game)
        game_copy.play(move, is_test=True)
        return ChessRules.king_is_under_atk(game_copy, game.is_white_turn)
