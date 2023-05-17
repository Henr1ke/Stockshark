from ppadb.client import Client as AdbClient
import time

# ADB Shell Command List:
# https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8


def connect():
    client = AdbClient(host="127.0.0.1", port=5037)

    devices = client.devices()

    if len(devices) == 0:
        print('No devices')
        quit()

    device = devices[0]

    print(f'Connected to {device}')

    return device, client


def take_photo(device):
    # open up camera app
    device.shell('input keyevent 27')

    # wait 5 seconds
    time.sleep(5)

    # take a photo with volume up
    device.shell('input keyevent 24')
    print('Taken a photo!')


def open_app(device, app_path):
    # para encontrar o nome do package da app pretendida instalei na Play Store
    # uma app chamada "Package Name Viewer 2.0"
    # encontrar a app (com.chessEngine é o nome do Android package):
    # cenasAfonso shell dumpsys package | findstr Activity | findstr com.chessEngine

    # open app in package @app_path
    device.shell('am start -n ' + app_path)


def screenshot(device, name):
    device.shell(f'screencap -p /sdcard/{name}.png')
    device.pull(f'/sdcard/{name}.png', f"chessPiecesImg/{name}.png")


def tap_play_button(device):
    device.shell('input tap 653 1777')


def tap_play_computer(device):
    device.shell('input tap 197 1469')


def tap_choose_computer(device):
    device.shell('input tap 533 1901')


def swipe(device, x1, y1, x2, y2):
    device.shell('input swipe ' + x1 + ' ' + y1 + ' ' + x2 + ' ' + y2)


def tap_screen(device, coords):
    command = f'input tap {coords[0]} {coords[1]}'
    print(command)
    device.shell(command)


if __name__ == '__main__':
    device, client = connect()
    # app_path = "com.chessEngine/.home.HomeActivity"
    # open_app(device, app_path)
    # time.sleep(5)
    # tap_play_computer(device)
    # time.sleep(5)
    # tap_choose_computer(device)
    # swipe(device, '900', '900', '30', '900')

    screenshot(device, "black_played_dark_to_white")

    # swipe(device, "550", "1900", "550", "900")
    # detect_board()
