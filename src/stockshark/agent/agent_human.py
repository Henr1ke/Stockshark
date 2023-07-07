from stockshark.agent.agent import Agent
from stockshark.chess_engine.chess_engine import ChessEngine


class AgentHuman(Agent):
    def gen_move(self, engine: ChessEngine) -> str:
        moves = engine.available_moves
        str_moves = [str(move) for move in moves]
        sorted_str = sorted(str_moves)
        while True:
            print(f"Select a move to make. Available moves: {sorted_str}")
            name = input("Move: ")
            if name in str_moves:
                idx = str_moves.index(name)
                return moves[idx]
            else:
                print(f"You did not introduced a valid move")
                print("Try again!")
