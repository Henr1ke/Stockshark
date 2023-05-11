import time

from ppadb.client import Client
from ppadb.device import Device
import scrcpy

# ADB Shell Command List:
# https://gist.github.com/Pulimet/5013acf2cd5b28e55036c82c91bd56d8


class ConnectorADB:
    def __init__(self, host="127.0.0.1", port=5037):
        client = Client(host=host, port=port)  # ADB Client

        devices = client.devices()

        if len(devices) == 0:
            print('No devices')
            quit()

        device = devices[0]
        client = scrcpy.Client(device=device)
        print(f'Connected to {device}')
        self.__device = device
        self.__client = client

    @property
    def device(self) -> Device:
        return self.__device

    @property
    def client(self) -> Client:
        return self.__client

    def tap_screen(self, x, y):
        command = f'input tap {x} {y}'
        print(command)
        self.device.shell(command)
        time.sleep(0.25)

    def input_text(self, txt: str):
        self.device.input_text(txt)

    def open_app(self, app_path):
        # para encontrar o nome do package da app pretendida instalei na Play Store
        # uma app chamada "Package Name Viewer 2.0"
        # encontrar a app (com.chessEngine é o nome do Android package):
        # adb shell dumpsys package | findstr Activity | findstr com.chessEngine

        # open app in package @app_path
        self.device.shell('am start -n ' + app_path)

    def screenshot(self, name="Screenshot"):
        self.device.shell(f'screencap -p /sdcard/{name}.png')
        self.device.pull(f'/sdcard/{name}.png', f"chessPiecesImg/{name}.png")

    def swipe_screen(self, x1, y1, x2, y2):
        self.device.shell('input swipe ' + x1 + ' ' + y1 + ' ' + x2 + ' ' + y2)

    def disconnect(self):
        self.client.remote_disconnect()
