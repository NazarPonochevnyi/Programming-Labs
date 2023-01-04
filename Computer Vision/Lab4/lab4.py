import cv2
import numpy as np
from colorgrad import colorgrad


def convert_to_rgb(image):
    """Converts the image to the RGB color space."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def convert_to_hsv(image):
    """Converts the image to the HSV color space."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

def convert_to_lab(image):
    """Converts the image to the L*a*b* color space."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

def smooth_by_channel(image):
    """Smooths the image by applying a Gaussian blur to each channel separately."""
    return cv2.GaussianBlur(image, (5, 5), 0)

def smooth_by_color_space(image):
    """Converts the image to the HSV and L*a*b* color spaces and smooths the value
    (V) and lightness (L*) channels."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    hsv[:,:,2] = cv2.GaussianBlur(hsv[:,:,2], (5, 5), 0)
    lab[:,:,0] = cv2.GaussianBlur(lab[:,:,0], (5, 5), 0)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR), cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def sharpen_by_channel(image):
    """Sharpens the image by applying the Laplacian operator to each channel separately."""
    return cv2.Laplacian(image, cv2.CV_64F)

def sharpen_by_color_space(image):
    """Converts the image to the HSV and L*a*b* color spaces and sharpens the value
    (V) and lightness (L*) channels using the Laplacian operator."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    hsv[:,:,2] = cv2.Laplacian(hsv[:,:,2], cv2.CV_64F)
    lab[:,:,0] = cv2.Laplacian(lab[:,:,0], cv2.CV_64F)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR), cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def equalize_histogram(image):
    """Equalizes the histogram of the image."""
    return cv2.equalizeHist(image)

def detect_contours_by_channel(image):
    """Detects contours in the image by applying the Canny edge detector to each channel
    separately."""
    return cv2.Canny(image, 100, 200)

def detect_contours_by_vector(image):
    """Detects contours in the image by applying the colorgrad function to the image."""
    _, _, contours = colorgrad(image)
    return contours

def compare_contours(image1, image2, image3):
    """Compares the results of the different contour detection methods by displaying the
    images side by side."""
    if image1.ndim == 2 and image2.ndim == 2:
        combined = np.hstack((image1, image2))
        cv2.imshow("Contour Comparison", combined)
    elif image1.ndim == 3 and image2.ndim == 3:
        combined = np.hstack((image1, image2, image3))
        cv2.imshow("Contour Comparison", combined)
    else:
        print("Error: incompatible array dimensions")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Load the image
    image = cv2.imread('pic1.png')

    # Convert the image to different color spaces
    rgb_image = convert_to_rgb(image)
    hsv_image = convert_to_hsv(image)
    lab_image = convert_to_lab(image)

    # Save the converted images
    cv2.imwrite('pic1_rgb.png', rgb_image)
    cv2.imwrite('pic1_hsv.png', hsv_image)
    cv2.imwrite('pic1_lab.png', lab_image)

    # Load the image
    image = cv2.imread('pic2.png')

    # Convert the image to different color spaces
    rgb_image = convert_to_rgb(image)
    hsv_image = convert_to_hsv(image)
    lab_image = convert_to_lab(image)

    # Perform image smoothing using component-by-component processing
    smoothed_image1 = smooth_by_channel(image)

    # Save the smoothed image
    cv2.imwrite('pic2_smooth_channel.png', smoothed_image1)

    # Smooth the image by converting it to HSV and Lab* color systems
    smoothed_image2, smoothed_image3 = smooth_by_color_space(image)

    # Save the smoothed images
    cv2.imwrite('pic2_smooth_hsv.png', smoothed_image2)
    cv2.imwrite('pic2_smooth_lab.png', smoothed_image3)

    # Sharpen the image using component-by-component processing
    sharpened_image1 = sharpen_by_channel(image)

    # Save the sharpened image
    cv2.imwrite('pic2_sharpen_channel.png', sharpened_image1)

    # Sharpen the image by converting it to HSV and Lab* color systems
    sharpened_image2, sharpened_image3 = sharpen_by_color_space(image)

    # Save the sharpened images
    cv2.imwrite('pic2_sharpen_hsv.png', sharpened_image2)
    cv2.imwrite('pic2_sharpen_lab.png', sharpened_image3)

    # Split the channels
    l_channel, a_channel, b_channel = cv2.split(lab_image)

    # Perform histogram equalization
    equalized_l_channel = equalize_histogram(l_channel)

    # Merge the channels back together and convert back to the RGB color space
    equalized_lab_image = cv2.merge((equalized_l_channel, a_channel, b_channel))
    equalized_image = cv2.cvtColor(equalized_lab_image, cv2.COLOR_LAB2BGR)

    # Save the equalized image
    cv2.imwrite('pic2_equalize.png', equalized_image)

    # Perform the detection of contours in the image component by component
    contours_image1 = detect_contours_by_channel(image)

    # Save the contours image
    cv2.imwrite('pic2_contours_channel.png', contours_image1)

    # Perform the detection of contours in the image considering it as a function vector
    contours_image2 = detect_contours_by_vector(image)

    # Save the contours image
    cv2.imwrite('pic2_contours_vector.png', contours_image2)

    # Compare the results of the different contour detection methods
    compare_contours(contours_image1, contours_image2, image)
