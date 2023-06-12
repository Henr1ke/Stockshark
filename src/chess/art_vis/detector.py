from typing import List, Tuple

import cv2
from numpy import ndarray

from chess.art_vis.image_processing import ImageProcessing
from chess.art_vis.visual_debug import VisualDebug


class Detector:
    @staticmethod
    def find_positions(board_img: ndarray, piece_img: ndarray, threshold: float = 0.55) -> List[Tuple[int, int]]:
        similarities = cv2.matchTemplate(board_img, piece_img, cv2.TM_CCOEFF_NORMED)
        detected_pixels = similarities >= threshold

        ys, xs = detected_pixels.nonzero()
        overlapping_boxes = [(x, y, piece_img.shape[1], piece_img.shape[0]) for x, y in zip(xs, ys)]

        # Group overlapping rectangles as one
        template_boxes, _ = cv2.groupRectangles(overlapping_boxes, 1, 1)

        return template_boxes


if __name__ == '__main__':
    pass
