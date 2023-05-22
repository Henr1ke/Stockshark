import time
from typing import Optional

from ppadb.client import Client
from ppadb.device import Device
import pathlib


class DaoADB:
    WAIT_TIME = 4
    APP_BOOT_TIME = 10

    def __init__(self):
        self.__client: Optional[Client] = None
        self.__device: Optional[Device] = None
        self.__is_connected: bool = False

    @property
    def client(self) -> Optional[Client]:
        return self.__client

    @property
    def device(self) -> Optional[Device]:
        return self.__device

    @property
    def is_connected(self) -> bool:
        return self.__is_connected

    def connect(self, host: str = "127.0.0.1", port: int = 5037) -> bool:
        if self.__is_connected:
            self.disconnect()

        client = Client(host=host, port=port)
        devices = client.devices()

        if len(devices) == 0:
            return False

        self.__client = client
        self.__device = devices[0]
        self.__is_connected = True

        return True

    def disconnect(self) -> None:
        if self.__client is not None:
            self.__client.remote_disconnect()

        self.__client = None
        self.__device = None
        self.__is_connected = False

    def tap_screen(self, x: int, y: int) -> None:
        self.__device.input_tap(x, y)
        time.sleep(DaoADB.WAIT_TIME)

    def swipe_screen(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.__device.input_swipe(x1, y1, x2, y2, 0.25)
        time.sleep(DaoADB.WAIT_TIME)

    def screenshot(self, folder: str = "screenshots", filename: str = "Screenshot") -> None:
        current_path = pathlib.Path(__file__).parent.resolve()
        self.__device.shell(f'screencap -p /sdcard/{filename}.png')
        self.__device.pull(f'/sdcard/{filename}.png', f"{current_path}/../../images/{folder}/{filename}.png")

    def input_text(self, text: str) -> None:
        self.__device.input_text(text)
        time.sleep(DaoADB.WAIT_TIME)

    def open_app(self, package_name: str) -> None:
        self.__device.shell(f"am start -n {package_name}")
        time.sleep(DaoADB.APP_BOOT_TIME)

    def get_device_model(self) -> str:
        print(self.__device.shell("wm size"))
        avd_name = self.__device.shell("getprop ro.kernel.qemu.avd_name").strip()
        if avd_name == "":
            return self.__device.shell("getprop ro.product.model").strip()
        return avd_name


if __name__ == '__main__':
    dao_adb = DaoADB()
    dao_adb.connect()
    dao_adb.get_device_model()
