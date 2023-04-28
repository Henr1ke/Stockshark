import random
from chessEngine.chess_components import Player, Simulator, Position, ChessException, Move


class PlayerHuman(Player):

    def gen_move(self, simulator: Simulator) -> Move:
        start_pos_list = self.get_available_pieces_pos(simulator)
        start_pos = random.choice(start_pos_list)

        end_pos_list = simulator.get_positions()


        return Move(start_pos, end_pos)


if __name__ == '__main__':
    s = Simulator((PlayerHuman(), PlayerHuman()))
    s.execute()

    pass
