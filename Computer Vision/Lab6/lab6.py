import cv2
import numpy as np
from graythresh import graythresh


def detect_brightness_differences(image, method):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if method == "LoG":
        diff_image = cv2.Laplacian(gray_image, cv2.CV_64F)
    elif method == "Canny":
        diff_image = cv2.Canny(gray_image, 100, 200)
    else:
        raise ValueError("Invalid method. Choose 'LoG' or 'Canny'.")
    return diff_image

def global_threshold(image, level):
    _, binary_image = cv2.threshold(image, level * 255, 255, cv2.THRESH_BINARY)
    return binary_image

def segment_by_watersheds_dt(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    binary_image = cv2.bitwise_not(binary_image)
    dist_transform = cv2.distanceTransform(binary_image, cv2.DIST_L2, 3)
    cv2.normalize(dist_transform, dist_transform, 0, 1.0, cv2.NORM_MINMAX)
    _, markers = cv2.connectedComponents(binary_image)
    markers = markers + 1
    markers[dist_transform > 0.5] = 0
    cv2.watershed(image, markers)
    mask = np.zeros_like(markers, dtype=np.uint8)
    mask[markers == -1] = 255
    return mask

def segment_by_watersheds_gradient(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    binary_image = cv2.bitwise_not(binary_image)
    sobel_x = cv2.Sobel(binary_image, cv2.CV_32F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(binary_image, cv2.CV_32F, 0, 1, ksize=3)
    gradient_magnitude = cv2.magnitude(sobel_x, sobel_y)
    cv2.normalize(gradient_magnitude, gradient_magnitude, 0, 1.0, cv2.NORM_MINMAX)
    _, markers = cv2.connectedComponents(binary_image)
    markers = markers + 1
    markers[gradient_magnitude > 0.5] = 0
    cv2.watershed(image, markers)
    mask = np.zeros_like(markers, dtype=np.uint8)
    mask[markers == -1] = 255
    return mask

def color_segmentation_kmeans(image, k):
    image = image.astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(image.reshape(-1, 3), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    mask = labels.reshape(image.shape[:2])
    mask = mask.astype(np.uint8)
    return mask


if __name__ == "__main__":
    image = cv2.imread("pic.3.tif")
    diff_image_log = detect_brightness_differences(image, "LoG")
    diff_image_canny = detect_brightness_differences(image, "Canny")
    cv2.imshow("Brightness Differences (LoG)", diff_image_log)
    cv2.imshow("Brightness Differences (Canny)", diff_image_canny)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    image = cv2.imread("pic.4.tif", 0)  # Read image in grayscale
    level = graythresh(image)
    binary_image = global_threshold(image, level)
    cv2.imshow("Global Threshold", binary_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    image = cv2.imread("pic.5.tif")
    mask = segment_by_watersheds_dt(image)
    cv2.imshow("Watershed Segmentation (Distance Transform)", mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    image = cv2.imread("pic.6.tif")
    mask = segment_by_watersheds_gradient(image)
    cv2.imshow("Watershed Segmentation (Gradient)", mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    image = cv2.imread("pic.8.jpg")
    mask = color_segmentation_kmeans(image, 3)  # 3 clusters
    cv2.imshow("Color Segmentation (K-Means)", mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
