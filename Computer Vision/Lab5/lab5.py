import cv2
import imutils
import numpy as np
from scipy import ndimage


def global_threshold(image):
     _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
     return binary_image

def dilate(image, kernel_size=3, iterations=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.dilate(image, kernel, iterations=iterations)

def erode(image, kernel_size=3, iterations=1):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.erode(image, kernel, iterations=iterations)

def mopen(image, kernel_size=3):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def mclose(image, kernel_size=3):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

def thin(image): 
    return cv2.ximgproc.thinning(image)

def skeletonize(img):
    skel = np.zeros(img.shape, np.uint8)
    while cv2.countNonZero(img) > 0:
        eroded = erode(img)
        iopen = mopen(img)
        temp = cv2.subtract(img, iopen)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()
    return skel

def select_cohesion_components(image, kernel_size=3):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary_image = global_threshold(gray_image)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    labels = ndimage.label(binary_image, structure=kernel)[0]
    for label in np.unique(labels):
        if label == 0:
            continue
        mask = np.zeros(gray_image.shape, dtype="uint8")
        mask[labels == label] = 255
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
    return image

def morphological_reconstruction(mask, marker, kernel_size=3):
    while True:
        expanded = dilate(marker, kernel_size=kernel_size, iterations=1)
        cv2.bitwise_and(src1=expanded, src2=mask, dst=expanded)
        if (marker == expanded).all():
            return expanded
        marker = expanded

def morphological_gradient(image, kernel_size=3):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

def top_hat(image, kernel_size=3):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)


if __name__ == "__main__":
    image1 = cv2.imread('pic.1.jpg', cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread('pic.2.jpg', cv2.IMREAD_GRAYSCALE)
    image3 = cv2.imread('pic.3.jpg', cv2.IMREAD_GRAYSCALE)
    image4 = cv2.imread('pic.4.jpg', cv2.IMREAD_GRAYSCALE)
    image5 = cv2.imread('pic.5.jpg')
    image6a = cv2.imread('pic.6a.tif', cv2.IMREAD_GRAYSCALE)
    image6b = cv2.imread('pic.6b.tif', cv2.IMREAD_GRAYSCALE)
    image7 = cv2.imread('pic.7.png', cv2.IMREAD_GRAYSCALE)
    image8 = cv2.imread('pic.8.png', cv2.IMREAD_GRAYSCALE)
    image9 = cv2.imread('pic.9.png', cv2.IMREAD_GRAYSCALE)
    image10 = cv2.imread('cameraman.tif', cv2.IMREAD_GRAYSCALE)
    image11 = cv2.imread('rice.png', cv2.IMREAD_GRAYSCALE)
    image12 = cv2.imread('pic.10.png', cv2.IMREAD_GRAYSCALE)

    # Apply the dilate function to image1
    image1 = global_threshold(image1)
    dilated_image1 = dilate(image1, kernel_size=2, iterations=1)
    cv2.imwrite('pic.1_dilate.jpg', dilated_image1)

    # Apply the erode function to image2
    image2 = global_threshold(image2)
    eroded_image2 = erode(image2, kernel_size=11, iterations=1)
    cv2.imwrite('pic.2_erode.jpg', eroded_image2)
    
    # Apply the open function to image3
    image3 = global_threshold(image3)
    opened_image3 = mopen(image3, kernel_size=3)
    cv2.imwrite('pic.3_open.jpg', opened_image3)

    # Apply the close function to image3
    closed_image3 = mclose(opened_image3, kernel_size=3)
    cv2.imwrite('pic.3_close.jpg', closed_image3)
    
    # Apply the thin function to image3
    thinned_image3 = thin(closed_image3)
    cv2.imwrite('pic.3_thin.jpg', thinned_image3)
    
    # Apply the skeletonize function to image4
    image4 = global_threshold(image4)
    skeletonized_image4 = skeletonize(image4)
    cv2.imwrite('pic.4_skeletonize.jpg', skeletonized_image4)
    
    # Apply the select_cohesion_components function to image5
    cohesion_components = select_cohesion_components(image5)
    cv2.imwrite('pic.5_cohesion_components.jpg', cohesion_components)
    
    # Apply the morphological_reconstruction function to image6a and image6b
    image6a = global_threshold(image6a)
    image6b = global_threshold(image6b)
    image6b = mopen(image6b, kernel_size=9)
    reconstructed_image6 = morphological_reconstruction(image6a, image6b)
    cv2.imwrite('pic.6_reconstruct.jpg', reconstructed_image6)

    # Apply the morphological_reconstruction function to image7
    image7 = global_threshold(image7)
    opened_image7 = cv2.morphologyEx(image7, cv2.MORPH_OPEN, np.ones((10, 1)))
    reconstructed_image7 = morphological_reconstruction(image7, opened_image7)
    cv2.imwrite('pic.7_reconstruct.jpg', reconstructed_image7)

    # Apply the halftone dilate function to image8
    halftone_dilated_image8 = dilate(image8, kernel_size=9, iterations=1)
    cv2.imwrite('pic.8_halftone_dilate.jpg', halftone_dilated_image8)

    # Apply the halftone erode function to image8
    halftone_eroded_image8 = erode(image8, kernel_size=9, iterations=1)
    cv2.imwrite('pic.8_halftone_erode.jpg', halftone_eroded_image8)

    # Apply the halftone open function to image9
    halftone_opened_image9 = mopen(image9, kernel_size=9)
    cv2.imwrite('pic.9_halftone_open.jpg', halftone_opened_image9)

    # Apply the halftone close function to image9
    halftone_closed_image9 = mclose(halftone_opened_image9, kernel_size=9)
    cv2.imwrite('pic.9_halftone_close.jpg', halftone_closed_image9)

    # Apply the morphological_gradient function to cameraman
    morphological_gradient_cameraman = morphological_gradient(image10)
    cv2.imwrite('cameraman_morphological_gradient.jpg', morphological_gradient_cameraman)

    # Apply the top_hat function to rice
    top_hat_rice = top_hat(image11, kernel_size=18)
    cv2.imwrite('rice_top_hat.jpg', top_hat_rice)

    # Apply the morphological halftone reconstruction function to pic.10
    eroded_image12 = cv2.erode(image12, np.ones((1, 9)))
    morphological_halftone_reconstructed_image12 = morphological_reconstruction(eroded_image12, image12)
    cv2.imwrite('pic.10_morphological_halftone_reconstruct.jpg', morphological_halftone_reconstructed_image12)
