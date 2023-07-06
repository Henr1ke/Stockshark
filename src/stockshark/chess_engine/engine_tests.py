import random
import time
from copy import copy
from typing import Type

from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.chess_engine.python_chess_engine import PythonChessEngine
from stockshark.chess_engine.stockshark_engine import StocksharkEngine


def run_random(engine: ChessEngine):
    for i in range(1000):
        print(engine.fen)

        print(f"{engine.attacked_tiles = }")

        avail_moves = engine.available_moves
        print(f"{avail_moves = }")

        if len(avail_moves) == 0:
            break

        m = random.choice(avail_moves)
        print(m)

        engine.play(m)
        print()

    print()
    print("engine over!")
    print(engine.fen)


def compare_runs(engineType1: Type[ChessEngine], engineType2: Type[ChessEngine]):
    engine1 = engineType1()
    engine2 = engineType2()

    for i in range(1000):
        print(engine1.fen)

        same_attacked_tiles = sorted(engine1.attacked_tiles) == sorted(engine2.attacked_tiles)
        print(f"{same_attacked_tiles = }")
        if not same_attacked_tiles:
            print(f"{engine1.attacked_tiles = }")
            print(f"{engine2.attacked_tiles = }")
            break

        same_avail_moves = sorted(engine1.available_moves) == sorted(engine2.available_moves)
        print(f"{same_avail_moves = }")
        if not same_avail_moves or len(engine1.available_moves) == 0:
            print(f"{engine1.available_moves = }")
            print(f"{engine2.available_moves = }")
            break

        m = random.choice(engine1.available_moves)
        print(m)
        engine1.play(m)
        engine2.play(m)
        print()

    print()
    print("engine over!")
    print(engine1.fen)


def perft(fen: str, engineType1: Type[ChessEngine], engineType2: Type[ChessEngine]):
    def move_gen(depth, engine: ChessEngine):
        if depth == 0:
            return 1

        num_pos = 0
        for move in engine.available_moves:
            engine_copy = copy(engine)
            engine_copy.play(move)
            num_moves = move_gen(depth - 1, engine_copy)
            num_pos += num_moves
        return num_pos

    engine1 = engineType1(fen)
    engine1.play("c1d2")

    engine2 = engineType2(fen)
    engine2.play("c1d2")

    print(engine1.fen)

    for move in engine1.available_moves:
        engine_copy = copy(engine1)
        engine_copy.play(move)
        count1 = move_gen(1, engine_copy)

        engine_copy = copy(engine2)
        engine_copy.play(move)
        count2 = move_gen(1, engine_copy)

        print(f"{move} - {count1} / {count2}")


def __time_run_moves(engineType: Type[ChessEngine], moves: list):
    engine = engineType()
    ti = time.time()
    for move in moves:
        engine.play(move)
    return time.time() - ti


def get_run_moves_avg_time(engineType: Type[ChessEngine], moves: list, num_runs: int):
    times = []
    print()
    for i in range(num_runs):
        times.append(__time_run_moves(engineType, moves))
        print(f"run {i + 1} - {times[-1]}")
    return sum(times) / len(times)


if __name__ == '__main__':
    # engine = PythonChessEngine()
    # engine = StockfishEngine()
    # engine = StocksharkEngine()
    #
    # run_random(engine)

    fen = "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8"
    perft(fen, PythonChessEngine, StocksharkEngine)

    # compare_runs(PythonChessEngine, StocksharkEngine)

    # moves = ['d2d3', 'b8a6', 'e1d2', 'b7b6', 'c2c3', 'g7g5', 'h2h3', 'd7d6', 'd2c2', 'f7f6', 'c3c4', 'b6b5', 'c2b3',
    #          'a6b8', 'c1e3', 'a7a6', 'c4b5', 'a6a5', 'e3a7', 'e7e6', 'b1d2', 'c8d7', 'a7e3', 'a8a7', 'e3g5', 'c7c6',
    #          'd3d4', 'c6c5', 'a1c1', 'f8e7', 'f2f4', 'd7c6', 'c1b1', 'f6f5', 'e2e3', 'c6e4', 'b3a3', 'a7c7', 'd1c2',
    #          'c7b7', 'd4c5', 'b8c6', 'g5h6', 'e7g5', 'a3a4', 'b7b8', 'c2b3', 'd8f6', 'g2g3', 'd6c5', 'b3d3', 'g5h6',
    #          'd3e4', 'g8e7', 'e4d3', 'f6c3', 'd3d4', 'b8c8', 'd4b4', 'c3d3', 'b4c5', 'c6d8', 'b1a1', 'c8c5', 'e3e4',
    #          'd8f7', 'h3h4', 'c5c3', 'a1c1', 'h6f8', 'c1e1', 'c3b3', 'f1h3', 'e7g6', 'g1e2', 'b3c3', 'e1b1', 'e6e5',
    #          'e2d4', 'd3c2', 'd4b3', 'f5e4', 'b1c1', 'g6h4', 'b5b6', 'c3c5', 'd2b1', 'c2g2', 'g3h4', 'h7h6', 'h4h5',
    #          'g2h2', 'h3f1', 'h8g8', 'f1a6', 'g8g7', 'c1f1', 'c5c4', 'a4a5', 'h2e2']
    #
    # # engineType = PythonChessEngine
    # engineType = StockfishEngine
    # # engineType = StocksharkEngine
    # avg = get_run_moves_avg_time(engineType, moves, 30)
    # print()
    # print(f"avg time: {avg}")

#   num_runs = 30
#   PythonChessEngine = 0.015363949537277221
#   StockfishEngine = 11.047215700149536
#   StocksharkEngine = 1.4375652154286702
