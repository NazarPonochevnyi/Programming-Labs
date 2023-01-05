import cv2
import numpy as np

def detect_brightness_differences(image, method):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply method to detect brightness differences
    if method == "LoG":
        # Laplacian of Gaussian
        diff_image = cv2.Laplacian(gray_image, cv2.CV_64F)
    elif method == "Canny":
        # Canny edge detector
        diff_image = cv2.Canny(gray_image, 100, 200)
    else:
        raise ValueError("Invalid method. Choose 'LoG' or 'Canny'.")
        
    return diff_image

# Example usage:
image = cv2.imread("pic.3.tif")
diff_image = detect_brightness_differences(image, "LoG")
cv2.imshow("Brightness Differences (LoG)", diff_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


import cv2

def global_threshold(image, level):
    # Threshold image
    _, binary_image = cv2.threshold(image, level * 255, 255, cv2.THRESH_BINARY)
    return binary_image

# Example usage:
image = cv2.imread("pic.4.tif", 0)  # Read image in grayscale
level = graythresh(image)
binary_image = global_threshold(image, level)
cv2.imshow("Global Threshold", binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


import cv2
import numpy as np

def segment_by_watersheds_dt(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold image
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Invert image
    binary_image = cv2.bitwise_not(binary_image)
    
    # Compute distance transform
    dist_transform = cv2.distanceTransform(binary_image, cv2.DIST_L2, 3)
    
    # Normalize distance transform
    cv2.normalize(dist_transform, dist_transform, 0, 1.0, cv2.NORM_MINMAX)
    
    # Perform watershed
    _, markers = cv2.connectedComponents(binary_image)
    markers = markers + 1
    markers[dist_transform > 0.5] = 0
    cv2.watershed(image, markers)
    
    # Generate mask
    mask = np.zeros_like(markers, dtype=np.uint8)
    mask[markers == -1] = 255
    
    return mask

# Example usage:
image = cv2.imread("pic.5.tif")
mask = segment_by_watersheds_dt(image)
cv2.imshow("Watershed Segmentation (Distance Transform)", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()


import cv2
import numpy as np

def segment_by_watersheds_gradient(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold image
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Invert image
    binary_image = cv2.bitwise_not(binary_image)
    
    # Compute gradient magnitude
    sobel_x = cv2.Sobel(binary_image, cv2.CV_32F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(binary_image, cv2.CV_32F, 0, 1, ksize=3)
    gradient_magnitude = cv2.magnitude(sobel_x, sobel_y)
    
    # Normalize gradient magnitude
    cv2.normalize(gradient_magnitude, gradient_magnitude, 0, 1.0, cv2.NORM_MINMAX)
    
    # Perform watershed
    _, markers = cv2.connectedComponents(binary_image)
    markers = markers + 1
    markers[gradient_magnitude > 0.5] = 0
    cv2.watershed(image, markers)
    
    # Generate mask
    mask = np.zeros_like(markers, dtype=np.uint8)
    mask[markers == -1] = 255
    
    return mask

# Example usage:
image = cv2.imread("pic.6.tif")
mask = segment_by_watersheds_gradient(image)
cv2.imshow("Watershed Segmentation (Gradient)", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()


import cv2
import numpy as np

def color_segmentation_kmeans(image, k):
    # Convert image to float32
    image = image.astype(np.float32)
    
    # Perform k-means clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(image.reshape(-1, 3), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Generate mask
    mask = labels.reshape(image.shape[:2])
    mask = mask.astype(np.uint8)
    
    return mask

# Example usage:
image = cv2.imread("pic.8.jpg")
mask = color_segmentation_kmeans(image, 3)  # 3 clusters
cv2.imshow("Color Segmentation (K-Means)", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
