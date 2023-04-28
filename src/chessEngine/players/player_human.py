from typing import Dict

from chessEngine.chess_components import Player, Simulator, Position, ChessException, Move, Piece


class PlayerHuman(Player):

    @staticmethod
    def get_start_pos(simulator: Simulator) -> Position:
        board = simulator.board

        positions = list(Player.get_available_pieces_pos(simulator).keys())

        while True:
            try:
                print()
                print(board)
                print()
                print(f"Select a piece to move. Positions to choose: {positions}")
                coord = input("Coordinate: ")
                start_pos = Position.coord_to_pos(coord)
                if start_pos in positions:
                    return start_pos
                else:
                    print(f"There is no {'white' if simulator.is_white_turn else 'black'} piece at \"{coord}\"")
                    print("Try again!")
            except ChessException as e:
                print(e)
                print("Try again!")

    @staticmethod
    def get_end_pos(simulator: Simulator, start_pos: Position) -> Position:
        board = simulator.board
        piece = board[start_pos]
        positions = simulator.get_positions(piece, start_pos)

        while True:
            try:
                print()
                print(board)
                print()
                print(f"Select where to play the selected piece. Positions to choose: {positions}")
                coord = input("Coordinate: ")
                end_pos = Position.coord_to_pos(coord)
                if end_pos in positions:
                    return end_pos
                else:
                    print(f"It is not possible to place the selected piece at \"{coord}\"")
                    print("Try again!")
            except ChessException as e:
                print(e)
                print("Try again!")

    def gen_move(self, simulator: Simulator) -> Move:
        start_pos = PlayerHuman.get_start_pos(simulator)
        end_pos = PlayerHuman.get_end_pos(simulator, start_pos)
        return Move(start_pos, end_pos)


def __main():
    simulator = Simulator((PlayerHuman(), PlayerHuman()))
    simulator.execute()


if __name__ == '__main__':
    __main()
    pass
