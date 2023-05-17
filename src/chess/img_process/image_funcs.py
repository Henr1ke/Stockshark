import cv2
import numpy as np
from numpy import ndarray


class ImageFuncs:
    @staticmethod
    def read(path: str) -> ndarray:
        return cv2.imread(path)

    @staticmethod
    def grayscale(img: ndarray) -> ndarray:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def morph_grad(img: ndarray, k_size: int = 3) -> ndarray:
        kernel = np.ones((k_size, k_size), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

    @staticmethod
    def crop(img: ndarray, x1: int, y1: int, x2: int, y2: int) -> ndarray:
        return img.copy()[y1: y2, x1: x2]

    @staticmethod
    def scale(img: ndarray, scale: float = 0.4) -> ndarray:
        dim = (int(img.shape[1] * scale), int(img.shape[0] * scale))
        return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
