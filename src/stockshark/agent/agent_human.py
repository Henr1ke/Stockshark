from stockshark.agent.agent import Agent
from stockshark.chess_engine.game import Game
from stockshark.util.chess_exception import ChessException
from stockshark.util.move import Move
from stockshark.util.tile import Tile


class AgentHuman(Agent):

    @staticmethod
    def get_start_tile(game: Game) -> Tile:
        tiles = list(game.get_available_pieces_tiles().values())

        while True:
            try:
                print(f"Select a piece to move. Tiles to choose: {[str(tile) for tile in tiles]}")
                name = input("Tile: ")
                start_tile = Tile(name)
                if start_tile in tiles:
                    return start_tile
                else:
                    print(f"There is no {'white' if game.is_white_turn else 'black'} piece at \"{name}\"")
                    print("Try again!")
            except ChessException as e:
                print(e)
                print("Try again!")

    @staticmethod
    def get_end_tile(game: Game, start_tile: Tile) -> Tile:
        piece = game.board[start_tile]
        moves = game.get_legal_piece_moves(piece)

        end_tiles = [move.end_tile for move in moves]
        while True:
            try:
                print(f"Select where to play the selected piece. Tiles to choose: {end_tiles}")
                name = input("Tile: ")
                end_tile = Tile(name)
                if end_tile in end_tiles:
                    return end_tile
                else:
                    print(f"It is not possible to place the selected piece at \"{name}\"")
                    print("Try again!")
            except ChessException as e:
                print(e)
                print("Try again!")

    def gen_move(self, game: Game) -> Move:
        start_tile = AgentHuman.get_start_tile(game)
        end_tile = AgentHuman.get_end_tile(game, start_tile)
        return Move(start_tile, end_tile)
