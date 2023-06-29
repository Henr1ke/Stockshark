import random

from stockshark.chess_engine_2.chess_engine import ChessEngine
from stockshark.chess_engine_2.chess_package_engine import ChessPackageEngine
from stockshark.chess_engine_2.stockfish_engine import StockfishEngine


def run_random(game: ChessEngine):
    for i in range(500):
        print(game.fen)

        avail_moves = game.get_available_moves()
        print(avail_moves)

        if len(avail_moves) == 0:
            break

        m = random.choice(avail_moves)
        print(m)

        game.make_move(m)
        print()

    print()
    print("Game over!")
    print(game.fen)

if __name__ == '__main__':
    game = ChessPackageEngine()
    # game = StockfishEngine()

    run_random(game)
