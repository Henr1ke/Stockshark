import random
import time
from copy import copy
from typing import Type

from stockshark.chess_engine.chess_engine import ChessEngine
from stockshark.chess_engine.python_chess_engine import PythonChessEngine


def run_random(engine: ChessEngine):
    for i in range(500):
        print(engine.fen)

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


def test_pos_5_perft(engineType: Type[ChessEngine]):
    engine = engineType("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")

    for i in range(5):
        print(move_gen(i + 1, engine))


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


def perft(fen: str, engineType1: Type[ChessEngine], engineType2: Type[ChessEngine]):
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

    # test_pos_5_perft(StocksharkEngine)

    # compare_runs(PythonChessEngine, StocksharkEngine)

    moves = ["b2b3", "b8c6", "b1a3", "e7e6", "g2g4", "g7g5", "a3b5", "d8f6", "b5a7", "f6f2", "e1f2", "d7d5", "g1h3",
             "a8b8", "a7b5", "f8a3", "f2g2", "g8e7", "b5d6", "e8f8", "d6b5", "e7g6", "g2g1", "a3b4", "d2d3", "b4a3",
             "b3b4", "f8g7", "c1d2", "b7b6", "b5d6", "c8d7", "d2e3", "a3b4", "d1e1", "c6d4", "e1b4", "f7f6", "g1g2",
             "e6e5", "d6b5", "d4f3", "b4b2", "g7g8", "b5a3", "b8c8", "a1c1", "f3d2", "b2b4", "e5e4", "b4d2", "f6f5",
             "h1g1", "d7c6", "d2c3", "c6d7", "h3g5", "c7c5", "g5e6", "g6h4", "g2g3", "d7c6", "c3e1", "c8f8", "d3d4",
             "g8f7", "c2c3", "f8b8", "e3d2", "b8a8", "e2e3", "h7h5", "f1h3", "c5c4", "g4h5", "h8d8", "c1a1", "d8b8",
             "h3g2", "a8a7", "e6c5", "c6b7", "c5d3", "h4g6", "h2h4", "f7e6", "g1f1", "e4d3", "g2h1", "e6e7", "f1f3",
             "a7a3", "h1g2", "b8f8", "e1h1", "g6h4", "g3h2", "f8f6", "h1g1", "a3a2", "a1d1", "b7a8", "g1e1", "a8c6",
             "f3h3", "f6g6", "e1g1", "a2c2", "d1f1", "c6e8", "f1f3", "c2c3", "f3g3", "b6b5", "d2e1", "c3c2", "g1f1",
             "g6f6", "e1b4", "f6d6", "g3f3", "c2b2", "f1f2", "e7e6", "f3g3", "b2f2", "h3h4", "f2f4", "b4a5", "d6a6",
             "g2f1", "e6f7", "f1d3", "a6e6", "a5d8", "f4e4", "d3b1", "e6e5", "g3g7", "f7g7", "h4h3", "e8f7", "h2g1",
             "f7g8", "d8h4", "g7f8", "b1e4", "f8f7", "e4c2", "e5e6", "c2b3", "e6g6", "h4g3", "g6e6", "g3h4", "b5b4",
             "g1g2", "g8h7", "b3a2", "b4b3", "h4f6", "b3a2", "h3h1", "e6e7", "h5h6", "a2a1b", "g2f3", "e7e4", "h1c1",
             "e4e8", "c1d1", "f7f6", "f3e2", "h7g8", "d1b1", "e8e7", "e3e4", "e7b7", "e2f2", "g8e6", "f2g3", "d5e4",
             "b1b3", "e6c8", "g3h2", "f5f4", "b3c3", "f6g6", "h2g1", "c8d7", "g1g2", "b7b4", "c3d3", "g6f6", "g2f2",
             "a1b2", "d3e3", "b4b6", "e3d3", "d7a4", "d3g3", "b2a3", "g3e3", "a3c1", "e3a3", "a4d7", "a3a6", "b6c6",
             "f2e1", "c6b6", "e1f1", "f6g6", "f1g1", "b6e6", "a6a7", "c1d2", "a7a4", "d2c3", "g1f2", "g6g5", "f2g1",
             "c3b2", "a4a8", "e6f6", "g1g2", "e4e3", "a8g8", "g5h4", "g8g6", "f6g6", "g2f3", "d7b5", "f3e4", "f4f3",
             "e4f4", "g6g1", "f4f3", "b5c6", "f3f4", "g1g7", "f4e3", "h4g4", "e3e2", "c6f3", "e2e1", "f3h1", "e1f1",
             "b2a3", "f1f2", "c4c3", "f2e2", "a3d6", "e2d3", "d6b8", "d4d5", "h1f3", "h6g7", "f3d1", "d3e4", "g4h3",
             "g7g8b", "h3h4", "g8e6", "h4h5", "e6g4", "h5g6", "g4h3", "g6g7", "e4e3", "d1a4", "h3e6", "b8c7", "e3f3",
             "a4d7", "f3e4", "c7d8", "e4d3", "d8g5", "e6f7", "g5c1", "d5d6", "c1e3", "d3c4", "d7h3", "c4b3", "h3c8",
             "d6d7", "c8b7", "d7d8r", "c3c2", "d8a8", "b7e4", "f7e8", "e3f4", "a8a7", "g7g8", "a7b7", "f4g3", "b3c3",
             "g3d6", "c3b2", "d6c5", "b2b3", "e4d3", "b7b6", "c2c1n", "b3b2", "c5d4", "b2c1", "d4f2", "b6f6", "d3e4",
             "f6f3", "e4g6", "f3f5", "f2h4", "f5f8", "g8g7", "c1d2", "g6e8", "f8f5", "e8f7", "d2c2", "h4e1", "f5f4",
             "g7h7", "f4a4", "f7h5", "a4b4", "e1c3", "b4g4", "c3a5", "c2b2", "a5e1", "b2c1", "e1a5", "g4g8", "h5e8",
             "g8g7", "h7g7", "c1b1", "g7f8", "b1c1", "f8g7", "c1d1", "g7g6", "d1c1", "a5c3", "c1b1", "e8c6", "b1a2",
             "g6f5", "a2a3", "c3b4", "a3a2", "b4d2", "a2b2", "c6e4", "b2a2", "d2a5", "a2b2", "f5g5", "b2a2", "g5f4",
             "a2a1", "a5b6", "a1b2", "e4f3", "b2a3", "f3e2", "a3b3", "b6c5", "b3a2", "f4f3", "a2b3", "e2c4", "b3c4",
             "c5e3", "c4d3", "e3c5", "d3c3", "f3e3", "c3b3", "c5d6", "b3a2", "d6g3", "a2a3", "g3b8", "a3a2", "e3d3",
             "a2a1", "d3d2", "a1b1", "d2e3", "b1c1", "e3d3", "c1b2", "d3d2", "b2a2", "d2c3", "a2a3", "c3c4", "a3a4",
             "b8f4", "a4a5", "f4g5", "a5a6", "c4c5", "a6b7", "g5f6", "b7c8", "f6g5", "c8d7", "g5e3", "d7e6", "c5b5",
             "e6d5", "e3f4", "d5e6", "f4h6", "e6e7", "b5a5", "e7f6", "h6c1", "f6g6", "c1d2", "g6h7", "d2e3", "h7g7",
             "e3c1", "g7f6", "c1h6", "f6e7", "a5a4", "e7e8", "h6g5", "e8f8", "a4b5", "f8f7", "b5b4", "f7e6", "g5d2",
             "e6f6", "b4a3", "f6f7", "d2a5", "f7e8", "a5c7", "e8e7", "a3b2", "e7e8", "c7f4", "e8d7", "b2a3", "d7c6",
             "f4c7", "c6b5", "c7g3", "b5a5", "a3a2", "a5a6", "g3d6", "a6a7", "a2a1", "a7b6", "d6g3", "b6c5", "g3b8",
             "c5d5", "b8d6", "d5d6", "a1a2", "d6c5", "a2a3", "c5c6", "a3b3", "c6d7", "b3a3", "d7e8", "a3b2", "e8f8",
             "b2a1", "f8g7", "a1b1", "g7f8", "b1a2", "f8e8", "a2b2", "e8d8", "b2c2", "d8c8", "c2b3", "c8d8", "b3a3",
             "d8e7", "a3b4", "e7f7", "b4a3", "f7e8", "a3b3"]
    engineType = PythonChessEngine
    # engineType = StocksharkEngine
    # engineType = StocksharkEngine
    avg = get_run_moves_avg_time(engineType, moves, 30)
    print()
    print(f"avg time: {avg}")

    pass

#   num_runs = 30
#   PythonChessEngine = 0.015363949537277221    0.0600657065709432
#   StockfishEngine = 11.047215700149536
#   StocksharkEngine = 1.595009740193685    3.3955979983011884
#
# stockshark perft results test position 5:
# 1 : 44
# 2 : 1486
# 3 : 62379
