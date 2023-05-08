# from copy import copy
# from typing import Dict, Optional, List, Union, Tuple
#
# from chess.piece.king import King
# from chess.piece.pawn import Pawn
# from chess.piece.piece import Piece
# from chess.piece.queen import Queen
# from chess.piece.rook import Rook
# from chess.player.player import Player
# from chess.util.chessException import ChessException
# from chess.util.constants import CHAR_TO_PIECE_CLASS, FILE_LETTERS
# from chess.util.move import Move
# from chess.util.position import Position
#
# class Game():
#     def __init__(self, fen_str: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
#         fen_str_fields = fen_str.split()
#
#         self.__board: Board = build_board(fen_str_fields[0])
#
#         self.__is_white_turn: bool = True if fen_str_fields[1] == "w" else False
#
#         self.__castlings: str = fen_str_fields[2]
#
#         self.__en_passant_target: Optional[Position] = None if fen_str_fields[3] == "-" \
#             else Position.coord_to_pos(fen_str_fields[3])
#
#         self.__halfclock: int = int(fen_str_fields[4])
#         self.__fullclock: int = int(fen_str_fields[5])
#
#         self.__pieces_positions: Dict[Piece, List[Position]] = dict()
#
#
# class Board:
#
#     def __init__(self, fen_str: str = "8/8/8/8/8/8/8/8") -> None:
#
#         self.__pieces_pos: Dict[bool, Dict[Piece, Position]] = {True: dict(), False: dict()}
#         self.__kings_pos: Dict[bool, Position] = dict()
#         self.__tiles: List[List[Optional[Piece]]] = [[None] * 8 for _ in range(8)]
#
#         for row, fen_substr in enumerate(fen_str.split("/")[::-1]):
#             col = 0
#             for char in fen_substr:
#                 if char.isdigit():
#                     col += int(char)
#
#                 else:
#                     piece_class = CHAR_TO_PIECE_CLASS[char.lower()]
#                     is_white = char.isupper()
#                     piece = piece_class(is_white)
#
#                     self.add_piece((col, row), piece)
#                     col += 1
#
#     def __getitem__(self, idx_val: Union[str, Position, Tuple[int, int]]) -> Optional[Piece]:
#         pos = Board.__idx_val_to_pos(idx_val)
#         return self.__tiles[8 - 1 - pos.row][pos.col]
#
#     def __copy__(self) -> Board:
#         cls = self.__class__
#         board = cls.__new__(cls)
#         for key, value in self.__dict__.items():
#             if key == "_Board__tiles":
#                 tiles = [[piece for piece in row] for row in value]
#                 setattr(board, key, tiles)
#             elif key == "_Board__pieces_pos":
#                 pieces_pos = {k: {k2: v2 for k2, v2 in v.items()} for k, v in value.items()}
#                 setattr(board, key, pieces_pos)
#             elif key == "_Board__kings_pos":
#                 kings_pos = {k: v for k, v in value.items()}
#                 setattr(board, key, kings_pos)
#             else:
#                 setattr(board, key, copy(value))
#         return board
#
#     def __str__(self) -> str:
#         board_str = "═══╦══" + "═╤══" * (8 - 1) + "═╗\n"
#
#         for row in range(8 - 1, -1, -1):
#             board_str += f" {row + 1} ║ " + " │ ".join(
#                 " " if self[col, row] is None else str(self[col, row]) for col in range(8)
#             ) + " ║\n"
#
#         board_str += f"═══╬══{'═╪══' * (8 - 1)}═╣\n"
#         board_str += f"   ║ {' │ '.join(FILE_LETTERS)} ║"
#         return board_str
#
#     @staticmethod
#     def __idx_val_to_pos(idx_val: Union[str, Position, Tuple[int, int]]) -> Position:
#         if isinstance(idx_val, Position):
#             return idx_val
#
#         if isinstance(idx_val, str):
#             return Position.coord_to_pos(idx_val)
#
#         return Position(idx_val[0], idx_val[1])
#
#     def add_piece(self, idx_val: Union[str, Position, Tuple[int, int]], piece: Piece) -> None:
#         if not isinstance(piece, Piece):
#             raise ChessException(f"Must add a Piece object to the board, got {piece} of type {type(piece)}")
#
#         pos = self.__idx_val_to_pos(idx_val)
#         if self[pos] is not None:
#             self.clear_pos(pos)
#
#         if isinstance(piece, King):
#             if self.__kings_pos.get(piece.is_white) is not None:
#                 raise ChessException(f"The board already contains a king, it is not allowed to add another")
#             self.__kings_pos[piece.is_white] = pos
#
#         self.__tiles[8 - 1 - pos.row][pos.col] = piece
#         self.__pieces_pos[piece.is_white][piece] = pos
#
#     def make_move(self, move: Move) -> Piece:
#         piece = self[move.start_pos]
#         if not isinstance(piece, Piece):
#             raise ChessException("There is no piece on the move starting position")
#
#         if self[move.end_pos] is not None:
#             self.clear_pos(move.end_pos)
#
#         self.__tiles[8 - 1 - move.start_pos.row][move.start_pos.col] = None
#         self.__tiles[8 - 1 - move.end_pos.row][move.end_pos.col] = piece
#
#         if isinstance(piece, King):
#             self.__kings_pos[piece.is_white] = move.end_pos
#
#         self.__pieces_pos[piece.is_white][piece] = move.end_pos
#         return piece
#
#     def clear_pos(self, idx_val: Union[str, Position, Tuple[int, int]]) -> None:
#         pos = self.__idx_val_to_pos(idx_val)
#         piece = self.__tiles[8 - 1 - pos.row][pos.col]
#         self.__tiles[8 - 1 - pos.row][pos.col] = None
#
#         if piece is not None:
#             self.__pieces_pos[piece.is_white].pop(piece)
#             if isinstance(piece, King):
#                 self.__kings_pos.pop(piece.is_white, None)
#
#     def get_pieces_pos(self, is_white: bool) -> Dict[Piece, Position]:
#
#         return copy(self.__pieces_pos[is_white])
#
#     def get_king_pos(self, is_white: bool) -> Position:
#         return self.__kings_pos[is_white]
#
#     def gen_fen_str(self) -> str:
#         piece_class_to_char = {val: key for (key, val) in CHAR_TO_PIECE_CLASS.items()}
#
#         fen_substrs = []
#
#         for i, row in enumerate(self.__tiles):
#             fen_substr = ""
#             tile_skips = 0
#             for piece in row:
#                 if piece is None:
#                     tile_skips += 1
#                 else:
#                     if tile_skips > 0:
#                         fen_substr += str(tile_skips)
#                         tile_skips = 0
#                     letter = piece_class_to_char[type(piece)]
#                     fen_substr += letter.upper() if piece.is_white else letter.lower()
#
#             if tile_skips > 0:
#                 fen_substr += str(tile_skips)
#             fen_substrs.append(fen_substr)
#
#         return "/".join(fen_substrs)
#
#
# class Simulator:
#     def __init__(self, players: Tuple[Player, Player],
#                  fen_str: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
#
#         self.__players: Tuple[Player, Player] = players
#
#         fen_str_fields = fen_str.split()
#
#         self.__board: Board = Board(fen_str_fields[0])
#
#         self.__is_white_turn: bool = True if fen_str_fields[1] == "w" else False
#
#         self.__castlings: Dict[bool, List[bool]] = {True: ["K" in fen_str_fields[2], "Q" in fen_str_fields[2]],
#                                                     False: ["k" in fen_str_fields[2], "q" in fen_str_fields[2]], }
#
#         self.__en_passant_target: Optional[Position] = None if fen_str_fields[3] == "-" \
#             else Position.coord_to_pos(fen_str_fields[3])
#
#         self.__halfclock: int = int(fen_str_fields[4])
#         self.__fullclock: int = int(fen_str_fields[5])
#
#         self.__pieces_positions: Dict[Piece, List[Position]] = dict()
#
#     def __copy__(self):
#         cls = self.__class__
#         simulator = cls.__new__(cls)
#         for key, value in self.__dict__.items():
#             if key == "_Simulator__castlings":
#                 castlings = {k: [e for e in v] for k, v in value.items()}
#                 setattr(simulator, key, castlings)
#             elif key == "_Simulator__pieces_positions":
#                 pieces_positions = {k: [e for e in v] for k, v in value.items()}
#                 setattr(simulator, key, pieces_positions)
#             else:
#                 setattr(simulator, key, copy(value))
#         return simulator
#
#     @property
#     def players(self) -> Tuple[Player, Player]:
#         return self.__players
#
#     @property
#     def board(self) -> Board:
#         return copy(self.__board)
#
#     @property
#     def is_white_turn(self) -> bool:
#         return self.__is_white_turn
#
#     @property
#     def en_passant_target(self) -> Optional[Position]:
#         return self.__en_passant_target
#
#     @property
#     def halfclock(self) -> int:
#         return self.__halfclock
#
#     @property
#     def fullclock(self) -> int:
#         return self.__fullclock
#
#     def execute(self, log_game_info=False) -> None:
#         in_progress, draw, win_w, win_b = range(4)
#
#         if log_game_info:
#             print()
#             print(f"Simulator {self} started execution")
#
#         game_state = in_progress
#         while game_state == in_progress:
#             player = self.__players[0 if self.__is_white_turn else 1]
#
#             if log_game_info:
#                 print()
#                 print(f"{'White' if self.__is_white_turn else 'Black'} turn to play")
#                 print(f"halfclock: {self.__halfclock}, fullclock: {self.__fullclock}")
#                 print(self.__board)
#
#             is_valid_move = False
#             while not is_valid_move:
#                 move = player.gen_move(copy(self))
#
#                 if log_game_info:
#                     print()
#                     print(f"{'White' if self.__is_white_turn else 'Black'} player chose the move [{move}]")
#
#                 try:
#                     self.play(move)
#                     is_valid_move = True
#
#                     if log_game_info:
#                         print(f"The move was played")
#
#                 except ChessException as e:
#                     print(e)
#                     if log_game_info:
#                         print(f"The move was not played")
#
#             pieces_pos = self.__board.get_pieces_pos(self.__is_white_turn)
#             can_make_move = False
#             for piece, pos in pieces_pos.items():
#                 if len(self.get_positions(piece, pos)) > 0:
#                     can_make_move = True
#                     break
#
#             if not can_make_move:
#                 if self.__king_is_under_atk(self.is_white_turn):
#                     game_state = win_b if self.__is_white_turn else win_w
#                 else:
#                     game_state = draw
#
#             elif self.__halfclock >= 100:
#                 game_state = draw
#
#         if log_game_info:
#             print()
#             if game_state == draw:
#                 print(f"Game ended in a draw")
#             else:
#                 winner, loser = ("white", "black") if game_state == win_w else ("black", "white")
#                 print(f"Game ended with {winner} player check-mating {loser} player")
#             print(f"halfclock: {self.__halfclock}, fullclock: {self.__fullclock}")
#             print(self.__board)
#
#     def is_legal_move(self, move: Move) -> bool:
#         piece = self.__board[move.start_pos]
#         return piece is not None and piece.is_white is self.__is_white_turn and \
#             move.end_pos in self.get_positions(piece, move.start_pos)
#
#     def play(self, move: Move, check_if_legal: bool = True) -> None:
#         def pawn_actions(is_white: bool) -> Optional[Position]:
#             if move.end_pos == self.__en_passant_target:
#                 capt_piece_pos = move.end_pos + ((0, -1) if is_white else (0, 1))
#                 self.__board.clear_pos(capt_piece_pos)
#             elif move.end_pos.row == (7 if is_white else 0):
#                 self.__board.add_piece(move.end_pos, Queen(is_white))  # TODO its always promoting to queen
#
#             if abs(move.start_pos.row - move.end_pos.row) == 2:
#                 return move.end_pos + ((0, -1) if is_white else (0, 1))
#
#         def rook_actions(is_white: bool) -> None:
#             initial_row = 0 if is_white else 7
#             if move.start_pos.row == initial_row:
#                 if move.start_pos.col == 0:
#                     self.__castlings[is_white][0] = False
#                 elif move.start_pos.col == 7:
#                     self.__castlings[is_white][1] = False
#
#         def king_actions(is_white: bool) -> None:
#             if move.start_pos == Position(4, 0 if is_white else 7):
#                 self.__castlings[is_white] = [False, False]
#
#                 if move.end_pos.col == 2:
#                     start_pos = Position(0, move.end_pos.row)
#                     end_pos = move.end_pos + (1, 0)
#                     self.__board.make_move(Move(start_pos, end_pos))
#                     # rook = self.__board[start_pos]
#                     # self.__board[start_pos] = None
#                     # self.__board[move.end_pos + (1, 0)] = rook
#                 elif move.end_pos.col == 6:
#                     start_pos = Position(7, move.end_pos.row)
#                     end_pos = move.end_pos + (-1, 0)
#                     self.__board.make_move(Move(start_pos, end_pos))
#                     # rook = self.__board[start_pos]
#                     # self.__board[start_pos] = None
#                     # self.__board[move.end_pos + (-1, 0)] = rook
#
#         if check_if_legal and not self.is_legal_move(move):
#             raise ChessException(f"The move is not legal, got \"{str(move)}\"")
#
#         should_reset_halfclock = self.__board[move.end_pos] is not None
#
#         # Update self.__board
#         piece = self.__board.make_move(move)
#         # piece = self.__board[move.start_pos]
#         # self.__board[move.start_pos] = None
#         # self.__board[move.end_pos] = piece
#
#         # Update self.__en_passants and self.__castlings
#         e_p_target = None
#         if isinstance(piece, Pawn):
#             should_reset_halfclock = True
#             e_p_target = pawn_actions(piece.is_white)
#         elif isinstance(piece, Rook):
#             rook_actions(piece.is_white)
#         elif isinstance(piece, King):
#             king_actions(piece.is_white)
#         self.__en_passant_target = e_p_target
#
#         # Update self.__is_white_turn
#         self.__is_white_turn = not self.__is_white_turn
#
#         # Update self.__halfclock
#         if should_reset_halfclock:
#             self.__halfclock = 0
#         else:
#             self.__halfclock += 1
#
#         # Update self.__fullclock
#         if self.__is_white_turn:
#             self.__fullclock += 1
#
#         # Reset self.__possible_poss
#         self.__pieces_positions.clear()
#
#     def get_positions(self, piece: Piece, start_pos: Position) -> List[Position]:
#         legal_pos = self.__pieces_positions.get(piece)
#
#         if legal_pos is None:
#             possible_pos = piece.gen_positions(self.__board, start_pos)
#
#             if isinstance(piece, Pawn):
#                 # Adds en passant target to the possible positions if possible
#                 increments = ((-1, 1), (-1, 1)) if piece.is_white else ((1, -1), (-1, -1))
#                 for inc in increments:
#                     try:
#                         end_pos = start_pos + inc
#                         if end_pos == self.__en_passant_target:
#                             possible_pos.append(end_pos)
#                             break
#                     except ChessException:
#                         pass
#
#             if isinstance(piece, King):
#                 # Adds castling positions to the possible positions if possible
#                 castling_rights = self.get_castlings(piece.is_white)
#                 if castling_rights[0] and self.__board[1, start_pos.row] is None and \
#                         self.__board[2, start_pos.row] is None and self.__board[3, start_pos.row] is None:
#                     possible_pos.append(start_pos + (-2, 0))
#                 if castling_rights[1] and self.__board[5, start_pos.row] is None and \
#                         self.__board[6, start_pos.row] is None:
#                     possible_pos.append(start_pos + (2, 0))
#
#             # Only keeps the position if the move does not leave the king in check
#             legal_pos = [end_pos for end_pos in possible_pos
#                          if not self.__leaves_king_under_atk(Move(start_pos, end_pos), piece.is_white)]
#
#             # Updates the dictionary
#             self.__pieces_positions[piece] = legal_pos
#
#         return legal_pos
#
#     def get_castlings(self, is_white: bool) -> List[bool]:
#         return copy(self.__castlings[is_white])
#
#     def __leaves_king_under_atk(self, move: Move, is_white: bool) -> bool:
#         # Plays the move in a copy of the simulator
#         simulator = copy(self)
#         simulator.play(move, False)
#
#         return simulator.__king_is_under_atk(is_white)
#
#     def __king_is_under_atk(self, is_white: bool):
#         king_pos = self.__board.get_king_pos(is_white)
#         pieces_pos = self.__board.get_pieces_pos(not is_white)
#
#         for atk_piece, pos in pieces_pos.items():
#             if king_pos in atk_piece.gen_positions(self.__board, pos):
#                 return True
#         return False
