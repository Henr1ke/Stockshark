class DaoADB:
    def __init__(self):
        self.__client = None
        self.__device = None
        self.__is_connected: bool = False

    @property
    def client(self):
        return self.__client

    @property
    def device(self):
        return self.__device

    @property
    def is_connected(self) -> bool:
        return self.__is_connected

    def connect(self, host: str, port: int) -> bool:
        pass

    def disconnect(self) -> bool:
        pass

    def tap_screen(self, x: int, y: int) -> None:
        pass

    def swipe_screen(self, x1: int, x2: int, y1: int, y2: int):
        pass

    def screenshot(self, filename: str = "Screenshot") -> None:
        pass

    def input_tex(self, text: str) -> None:
        pass
