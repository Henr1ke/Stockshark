from chess.sim.game import Game
from chess.sim.state import State


class Visualizer:
    @staticmethod
    def show(game: Game):
        print()

        if game.state == State.IN_PROGRESS:
            print(f"{'White' if game.is_white_turn else 'Black'} turn to play")
        elif game.state == State.DRAW:
            print(f"Game ended in a draw")
        else:
            winner, loser = ("white", "black") if game.state == State.WIN_W else ("black", "white")
            print(f"Game ended with {winner} player check-mating {loser} player")
        print(f"halfclock: {game.halfclock}, fullclock: {game.fullclock}")
        print(game.board)


if __name__ == '__main__':
    game = Game()
    Visualizer.show(game)
