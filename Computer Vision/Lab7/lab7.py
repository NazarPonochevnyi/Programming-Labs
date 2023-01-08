import cv2
import numpy as np


def process_image(image):
    roi = image[100:200, 100:200]

    im = np.zeros(image.shape, np.uint8)
    noise = cv2.randn(im, (0), (99))
    image = image + noise
    rows, cols, _ = image.shape
    pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
    pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
    M = cv2.getAffineTransform(pts1, pts2)
    image = cv2.warpAffine(image, M, (cols, rows))

    res = cv2.matchTemplate(image, roi, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + 150, top_left[1] + 150)
    cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    return roi, image


if __name__ == "__main__":
    image = cv2.imread("cameraman.tif")

    roi, result = process_image(image)

    cv2.imwrite("roi.jpg", roi)
    cv2.imwrite("result.jpg", result)
