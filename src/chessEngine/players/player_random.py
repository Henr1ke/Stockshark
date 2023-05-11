# import random
#
# from chessEngine.chess_components import Player, Simulator, Position, ChessException, Move
# from chessEngine.players.player_human import PlayerHuman
#
#
# class PlayerRandom(Player):
#
#     def gen_move(self, simulator: Simulator) -> Move:
#         pieces_pos = self.get_available_pieces_pos(simulator)
#         piece, start_pos = random.choice(list(pieces_pos.items()))
#
#         end_pos_list = simulator.get_positions(piece, start_pos)
#         end_pos = random.choice(end_pos_list)
#
#         return Move(start_pos, end_pos)
#
#
# def human_vs_random():
#     s = Simulator((PlayerHuman(), PlayerRandom()))
#     s.execute()
#
#
# def random_vs_random():
#     s = Simulator((PlayerRandom(), PlayerRandom()))
#     s.execute(log_game_info=True)
#
#
# if __name__ == '__main__':
#     random_vs_random()
#     pass
