import pathlib
from typing import Tuple, List

import cv2
import numpy as np
from numpy import ndarray


class ImageProcessing:
    @staticmethod
    def read_img(filename: str, is_grayscale:bool = False) -> ndarray:
        current_path = pathlib.Path(__file__).parent.resolve()
        path = f"{current_path}/../../images/{filename}"
        return cv2.imread(path) if not is_grayscale else cv2.imread(path, cv2.IMREAD_GRAYSCALE)


    @staticmethod
    def write_img(filename: str, img: ndarray) -> None:
        current_path = pathlib.Path(__file__).parent.resolve()
        return cv2.imwrite(f"{current_path}/../../images/{filename}", img)

    @staticmethod
    def show(img: ndarray, title: str = "image") -> None:
        cv2.imshow(title, img)
        cv2.waitKey()
        cv2.destroyAllWindows()

    @staticmethod
    def grayscale(img: ndarray) -> ndarray:
        if len(img.shape) == 2:
            return img
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def morph_grad(img: ndarray, k_size: int = 3) -> ndarray:
        kernel = np.ones((k_size, k_size), np.uint8)
        return cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)

    @staticmethod
    def crop(img: ndarray, x1: int, y1: int, x2: int, y2: int) -> ndarray:
        return img.copy()[y1: y2, x1: x2]

    @staticmethod
    def scale(img: ndarray, scale: float) -> ndarray:
        dim = (int(img.shape[1] * scale), int(img.shape[0] * scale))
        return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    @staticmethod
    def resize(img: ndarray, final_shape: Tuple[int, int]) -> ndarray:
        def get_slice_coords(i_size, f_size) -> Tuple[int, int, int, int]:
            i_center = int(i_size / 2)
            f_center = int(f_size / 2)

            p_i_1 = max(i_center - f_center, 0)
            p_i_2 = min(p_i_1 + f_size, i_size)
            p_f_1 = max(f_center - i_center, 0)
            p_f_2 = min(p_f_1 + i_size, f_size)

            return p_i_1, p_i_2, p_f_1, p_f_2

        final_img = np.ones((*final_shape[::-1], *img.shape[2:]), dtype="uint8") * 255

        slice_h = get_slice_coords(img.shape[0], final_shape[1])
        slice_w = get_slice_coords(img.shape[1], final_shape[0])

        final_img[slice_h[2]:slice_h[3], slice_w[2]:slice_w[3]] = img[slice_h[0]:slice_h[1], slice_w[0]:slice_w[1]]
        return final_img

    @staticmethod
    def combine_imgs(img1: ndarray, img2: ndarray) -> ndarray:
        float_average = (img1 * 1.0 + img2 * 1.0) / 2
        return np.array(float_average, dtype="uint8")

    @staticmethod
    def get_px_similarities(img: ndarray, template: ndarray) -> ndarray:
        similarities = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        p_0_start = int(template.shape[0] / 2)
        p_0_end = template.shape[0] - p_0_start - 1
        p_1_start = int(template.shape[1] / 2)
        p_1_end = template.shape[1] - p_1_start - 1
        return np.pad(similarities, ((p_0_start, p_0_end), (p_1_start, p_1_end)), "constant")

    @staticmethod
    def locate(img: ndarray, template: ndarray, threshold: float = 0.55, margin=0) -> List[Tuple[int, int]]:
        if margin > 0:
            template = ImageProcessing.crop(template, margin, margin, template.shape[1] - margin,
                                            template.shape[0] - margin)

        similarities = ImageProcessing.get_px_similarities(img, template)
        half_shape = np.array(template.shape) / 2
        coordinates = []
        for i in range(64):  # Upper limit of loops to prevent infinite loop
            center = np.unravel_index(np.argmax(similarities), similarities.shape)
            if similarities[center] < threshold:
                break

            coordinates.append((center[1], center[0]))
            start_point = np.array(center - half_shape, dtype=int)[::-1]
            end_point = np.array(center + half_shape, dtype=int)[::-1]
            cv2.rectangle(similarities, start_point, end_point, 0, -1)

        return coordinates

    @staticmethod
    def get_value_count(img: ndarray, value: int) -> int:
        return int(np.sum(img == value))

    @staticmethod
    def get_square(img: ndarray, center: Tuple[int, int], side: int) -> ndarray:
        x1 = int(center[0] - side / 2)
        y1 = int(center[1] - side / 2)
        x2 = int(center[0] + side / 2)
        y2 = int(center[1] + side / 2)

        return ImageProcessing.crop(img, x1, y1, x2, y2)
