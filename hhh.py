from ppadb.client import Client as AdbClient
import time


def connect():
    adbClient = AdbClient(host="127.0.0.1", port=5037)

    devices = adbClient.devices()

    if len(devices) == 0:
        print('No devices')
        quit()

    adb_device = devices[0]

    print(f'Connected to {adb_device}')

    return adb_device, adbClient


def open_app(adb_device, app_path):
    # para encontrar o nome do package da app pretendida instalei na Play Store
    # uma app chamada "Package Name Viewer 2.0"
    # encontrar a app (com.chess é o nome do Android package):
    # adb shell dumpsys package | findstr Activity | findstr com.chess

    # open app in package @app_path
    adb_device.shell('am start -n ' + app_path)


def screenshot(adb_device):
    adb_device.shell('screencap -p /sdcard/screenshot.png')
    
def tap(adb_device, x, y):
    adb_device.shell(f"input tap {x} {y}")
    
def swipe(adb_device, xi, yi, xf, yf):
    adb_device.shell(f"input tap {xi} {yi} {xf} {yf}")

def text(adb_device, text):
    adb_device.shell(f"input text \"{text}\"")

def keyevent(adb_device, key_number):
    adb_device.shell(f"input keyevent {key_number}")

def tap_play_button(adb_device):
    tap(adb_device, 653, 1777)


def tap_play_computer(adb_device):
    tap(adb_device, 197, 1469)


def tap_choose_computer(adb_device):
    tap(adb_device, 533, 1901)


if __name__ == '__main__':
    device, client = connect()
    app_path = "com.chess/.home.HomeActivity"
    open_app(device, app_path)
    time.sleep(5)
    tap_play_computer(device)
    time.sleep(5)
    tap_choose_computer(device)
