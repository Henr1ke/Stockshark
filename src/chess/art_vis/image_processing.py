import pathlib
from typing import Tuple

import cv2
import numpy as np
from numpy import ndarray


class ImageProcessing:
    @staticmethod
    def read_img(folder: str, filename: str) -> ndarray:
        current_path = pathlib.Path(__file__).parent.resolve()
        return cv2.imread(f"{current_path}/../../images/{folder}/{filename}.png")

    @staticmethod
    def write_img(folder: str, filename: str, img: ndarray) -> None:
        current_path = pathlib.Path(__file__).parent.resolve()
        return cv2.imwrite(f"{current_path}/../../images/{folder}/{filename}.png", img)

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

    @staticmethod
    def resize(img: ndarray, final_shape: Tuple[int, int]) -> ndarray:
        def get_slice_coords(i_size, f_size) -> Tuple[int, int, int, int]:
            i_center = int(np.floor(i_size / 2))
            f_center = int(np.floor(f_size / 2))

            p_i_1 = max(i_center - f_center, 0)
            p_i_2 = min(p_i_1 + f_size, i_size)
            p_f_1 = max(f_center - i_center, 0)
            p_f_2 = min(p_f_1 + i_size, f_size)

            return (p_i_1, p_i_2, p_f_1, p_f_2)

        final_img = np.ones((*final_shape, *img.shape[2:]), dtype="uint8")

        slice_0 = get_slice_coords(img.shape[0], final_shape[0])
        slice_1 = get_slice_coords(img.shape[1], final_shape[1])

        final_img[slice_0[2]:slice_0[3], slice_1[2]:slice_1[3]] = img[slice_0[0]:slice_0[1], slice_1[0]:slice_1[1]]
        return final_img

    @staticmethod
    def combine_imgs(img1: ndarray, img2: ndarray) -> ndarray:
        float_mean = (img1 * 1.0 + img2 * 1.0) / 2
        return np.array(float_mean, dtype="uint8")

# if __name__ == '__main__':
#     img = ImageProcessing.read_img("screenshots", "sakjbafb")
#
#     print(img is None)
