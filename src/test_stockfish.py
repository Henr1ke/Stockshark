from stockfish import Stockfish

from stockshark.util.move import Move
from stockshark.util.tile import Tile

stockfish = Stockfish(path="stockfish/stockfish-windows-2022-x86-64-modern.exe")
stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
print(stockfish.get_board_visual())
move = Move(Tile("a2"), Tile("a4"))
stockfish.make_moves_from_current_position([str(move)])
print(stockfish.get_board_visual())

stockfish.set_fen_position()
stockfish.get_fen_position()
stockfish.make_moves_from_current_position()
stockfish.is_move_correct()
stockfish.get_what_is_on_square()
stockfish.will_move_be_a_capture()
stockfish.get_evaluation()
print(stockfish.get_board_visual())
