import cv2
from numpy import ndarray

from chess.adb.dao_adb import DaoADB


def printscreen() -> None:
    dao = DaoADB()
    dao.connect()
    dao.screenshot()


def debug_show_img(img: ndarray, title: str = "debug") -> None:
    cv2.imshow(title, img)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    printscreen()
    pass
