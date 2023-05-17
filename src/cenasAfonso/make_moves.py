# from img_to_FEN import get_board_coords
# from ppadb.client import Client as AdbClient
# from chessEngine.chess_components import Move, Position
#
#
# def connect():
#     client = AdbClient(host="127.0.0.1", port=5037)
#
#     devices = client.devices()
#
#     if len(devices) == 0:
#         print('No devices')
#         quit()
#
#     device = devices[0]
#
#     print(f'Connected to {device}')
#
#     return device, client
#
#
# def tap_screen(device, coords):
#     command = f'input tap {coords[0]} {coords[1]}'
#     print(command)
#     device.shell(command)
#
#
# def play(move: Move):
#     device, _ = connect()  # Deve ser chamado antes para estabelecer a conexão mais cedo
#
#     start_pos = move.start_pos
#     end_pos = move.end_pos
#
#     board_coords = get_board_coords()
#     botleft_corner = (board_coords[0], board_coords[1] + board_coords[3])
#     gap = board_coords[2]/8
#
#     pos = [start_pos, end_pos]
#     for p in pos:
#         file = p.col
#         rank = p.row
#
#         tap_x = int(botleft_corner[0] + gap*file + gap/2)
#         tap_y = int(botleft_corner[1] - gap*rank - gap/2)
#         tap_coords = (tap_x, tap_y)
#
#         tap_screen(device, tap_coords)
#
#
# if __name__ == "__main__":
#     move = Move(Position(1, 3), Position(1, 4))
#     play(move)
#     move = Move(Position(0, 3), Position(0, 4))
#     play(move)
