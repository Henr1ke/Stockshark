from chess.player.player import Player
from chess.chessGame.chess_game import ChessGame
from chess.util.chess_exception import ChessException
from chess.util.move import Move
from chess.util.position import Position


class PlayerHuman(Player):

    @staticmethod
    def get_start_pos(game: ChessGame) -> Position:
        board = game.board

        positions = list(game.get_available_pieces_pos().values())

        while True:
            try:
                print(f"Select a piece to move. Positions to choose: {[str(pos) for pos in positions]}")
                coord = input("Coordinate: ")
                start_pos = Position(coord)
                if start_pos in positions:
                    return start_pos
                else:
                    print(f"There is no {'white' if game.is_white_turn else 'black'} piece at \"{coord}\"")
                    print("Try again!")
            except ChessException as e:
                print(e)
                print("Try again!")

    @staticmethod
    def get_end_pos(game: ChessGame, start_pos: Position) -> Position:
        board = game.board
        piece = board[start_pos]
        positions = game.get_legal_piece_pos(piece)

        while True:
            try:
                print(
                    f"Select where to play the selected piece. Positions to choose: {[str(pos) for pos in positions]}")
                coord = input("Coordinate: ")
                end_pos = Position(coord)
                if end_pos in positions:
                    return end_pos
                else:
                    print(f"It is not possible to place the selected piece at \"{coord}\"")
                    print("Try again!")
            except ChessException as e:
                print(e)
                print("Try again!")

    def gen_move(self, game: ChessGame) -> Move:
        start_pos = PlayerHuman.get_start_pos(game)
        end_pos = PlayerHuman.get_end_pos(game, start_pos)
        return Move(start_pos, end_pos)
