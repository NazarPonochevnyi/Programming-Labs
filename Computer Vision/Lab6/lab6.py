import cv2
import imutils
import numpy as np
from scipy import ndimage
from skimage.feature import peak_local_max
from skimage.segmentation import watershed


def detect_brightness_differences(image, method):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    if method == "LoG":
        diff_image = cv2.Laplacian(gray_image, cv2.CV_64F)
    elif method == "Canny":
        diff_image = cv2.Canny(gray_image, 50, 100)
    else:
        raise ValueError("Invalid method. Choose 'LoG' or 'Canny'.")
    return diff_image

def global_threshold(image):
     _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
     return binary_image

def segment_by_watersheds_dt(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary_image = global_threshold(gray_image)
    D = ndimage.distance_transform_edt(binary_image)
    localMax = peak_local_max(D, indices=False, min_distance=20, labels=binary_image)
    markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
    labels = watershed(-D, markers, mask=binary_image)
    for label in np.unique(labels):
        if label == 0:
            continue
        mask = np.zeros(gray_image.shape, dtype="uint8")
        mask[labels == label] = 255
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(x), int(y)), int(r), (0, 0, 255), 2)
    return image

def segment_by_watersheds_gradient(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray_image, cv2.CV_32F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray_image, cv2.CV_32F, 0, 1, ksize=3)
    gradient_magnitude = cv2.magnitude(sobel_x, sobel_y)
    (minVal, maxVal) = (np.min(gradient_magnitude), np.max(gradient_magnitude))
    gradient = (255 * ((gradient_magnitude - minVal) / (maxVal - minVal)))
    gradient = gradient.astype("uint8")
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    gradient = cv2.morphologyEx(gradient, cv2.MORPH_CLOSE, sqKernel)
    binary_image = global_threshold(gradient)
    binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, sqKernel)
    binary_image = cv2.erode(binary_image, sqKernel)
    D = ndimage.distance_transform_edt(binary_image)
    localMax = peak_local_max(D, indices=False, min_distance=20, labels=binary_image)
    markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
    labels = watershed(-D, markers, mask=binary_image)
    plotted_circles = []
    for label in np.unique(labels):
        if label == 0:
            continue
        mask = np.zeros(gray_image.shape, dtype="uint8")
        mask[labels == label] = 255
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        ((x, y), r) = cv2.minEnclosingCircle(c)
        overlaps = False
        for (px, py, pr) in plotted_circles:
            if np.sqrt((x - px)**2 + (y - py)**2) < r + pr - 10:
                overlaps = True
                break
        if not overlaps:
            cv2.circle(image, (int(x), int(y)), int(r), (0, 0, 255), 2)
            plotted_circles.append((x, y, r))
    return image

def color_segmentation_kmeans(image, k):
    image = image.astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)
    _, labels, centers = cv2.kmeans(image.reshape(-1, 3), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape((image.shape))
    return segmented_image


if __name__ == "__main__":
    image = cv2.imread("pic.3.tif")
    diff_image_log = detect_brightness_differences(image, "LoG")
    diff_image_canny = detect_brightness_differences(image, "Canny")
    cv2.imshow("Brightness Differences (LoG)", diff_image_log)
    cv2.imshow("Brightness Differences (Canny)", diff_image_canny)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    image = cv2.imread("pic.4.tif", 0)  # Read image in grayscale
    binary_image = global_threshold(image)
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
    mask = color_segmentation_kmeans(image, 2)
    cv2.imshow("Color Segmentation (K-Means)", mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
