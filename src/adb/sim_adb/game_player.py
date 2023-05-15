from adb.identifier.identifier import Identifier
from adb.sim_adb.connector_ADB import ConnectorADB
from chessEngine.chess_components import Move


class GamePlayer:
    def __init__(self):
        self.__connector = ConnectorADB()

    @property
    def connector(self):
        return self.__connector

    def play(self, move: Move):
        # Needs a device != None (run connect() function)
        if self.connector.device is None:
            raise Exception("No connection established, please connect an ADB client")
        start_pos = move.start_pos
        end_pos = move.end_pos

        board_coords = Identifier.get_board_coords()
        botleft_corner = (board_coords[0], board_coords[1] + board_coords[3])
        gap = board_coords[2] / 8

        pos = [start_pos, end_pos]
        for p in pos:
            file = p.col
            rank = p.row

            tap_x = int(botleft_corner[0] + gap * file + gap / 2)
            tap_y = int(botleft_corner[1] - gap * rank - gap / 2)

            self.connector.tap_screen(tap_x, tap_y)

    def is_adv_white(self) -> bool:
        pass

    def get_adv_move(self) -> Move:
        pass
