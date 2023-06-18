from stockfish import Stockfish
from stockshark.util.move import Move
from stockshark.util.position import Position

stockfish = Stockfish(path="stockfish/stockfish-windows-2022-x86-64-modern.exe")
stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
print(stockfish.get_board_visual())
move = Move(Position("a2"), Position("a4"))
stockfish.make_moves_from_current_position([str(move)])
print(stockfish.get_board_visual())
