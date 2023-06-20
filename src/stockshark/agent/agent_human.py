from stockshark.agent.agent import Agent
from stockshark.chess_engine.game import Game
from stockshark.util.chess_exception import ChessException
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class AgentHuman(Agent):

    @staticmethod
    def get_start_pos(game: Game) -> Tile:
        positions = list(game.get_available_pieces_pos().values())

        while True:
            try:
                print(f"Select a piece to move. Positions to choose: {[str(pos) for pos in positions]}")
                coord = input("Coordinate: ")
                start_pos = Tile(coord)
                if start_pos in positions:
                    return start_pos
                else:
                    print(f"There is no {'white' if game.is_white_turn else 'black'} piece at \"{coord}\"")
                    print("Try again!")
            except ChessException as e:
                print(e)
                print("Try again!")

    @staticmethod
    def get_end_pos(game: Game, start_pos: Tile) -> Tile:
        piece = game.board[start_pos]
        moves = game.get_legal_piece_moves(piece)

        end_positions = [move.end_tile for move in moves]
        while True:
            try:
                print(
                    f"Select where to play the selected piece. Positions to choose: {end_positions}")
                coord = input("Coordinate: ")
                end_pos = Tile(coord)
                if end_pos in end_positions:
                    return end_pos
                else:
                    print(f"It is not possible to place the selected piece at \"{coord}\"")
                    print("Try again!")
            except ChessException as e:
                print(e)
                print("Try again!")

    def gen_move(self, game: Game) -> Move:
        start_pos = AgentHuman.get_start_pos(game)
        end_pos = AgentHuman.get_end_pos(game, start_pos)
        return Move(start_pos, end_pos)
