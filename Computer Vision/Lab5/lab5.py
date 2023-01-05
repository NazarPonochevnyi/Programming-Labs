import cv2
import numpy as np


def dilate(image, kernel_size=3, iterations=1):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(image, kernel, iterations=iterations)

def erode(image, kernel_size=3, iterations=1):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(image, kernel, iterations=iterations)

def mopen(image, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def mclose(image, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

def thin(image): 
    return cv2.ximgproc.thinning(image)

def skeletonize(image):
    ret, img = cv2.threshold(image, 127, 255, 0)
    skel = np.zeros(img.shape, np.uint8)
    while cv2.countNonZero(img) > 0:
        eroded = erode(img)
        iopen = mopen(img)
        temp = cv2.subtract(img, iopen)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()
    return skel

def select_cohesion_components(image):
    return cv2.connectedComponents(image)

def morphological_reconstruction(marker, mask, radius=1):
    kernel = np.ones(shape=(radius * 2 + 1,) * 2, dtype=np.uint8)
    while True:
        expanded = cv2.dilate(src=marker, kernel=kernel)
        cv2.bitwise_and(src1=expanded, src2=mask, dst=expanded)

        # Termination criterion: Expansion didn't change the image at all
        if (marker == expanded).all():
            return expanded
        marker = expanded

def halftone_dilate(image, kernel_size=3, iterations=1):
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    return cv2.dilate(image, kernel, iterations=iterations)

def halftone_erode(image, kernel_size=3, iterations=1):
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    return cv2.erode(image, kernel, iterations=iterations)

def halftone_open(image, kernel_size=3):
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def halftone_close(image, kernel_size=3):
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

def morphological_gradient(image):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    return cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

def top_hat(image, kernel_size=3):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)

def morphological_halftone_reconstruction(marker, mask):
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    return cv2.morphologyEx(marker, cv2.MORPH_HITMISS, kernel)


if __name__ == "__main__":
    # Read the images
    image1 = cv2.imread('pic.1.jpg', cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread('pic.2.jpg', cv2.IMREAD_GRAYSCALE)
    image3 = cv2.imread('pic.3.jpg', cv2.IMREAD_GRAYSCALE)
    image4 = cv2.imread('pic.4.jpg', cv2.IMREAD_GRAYSCALE)
    image5 = cv2.imread('pic.5.jpg', cv2.IMREAD_GRAYSCALE)
    image6a = cv2.imread('pic.6a.tif', cv2.IMREAD_GRAYSCALE)
    image6b = cv2.imread('pic.6b.tif', cv2.IMREAD_GRAYSCALE)
    image7 = cv2.imread('pic.7.png', cv2.IMREAD_GRAYSCALE)
    image8 = cv2.imread('pic.8.png', cv2.IMREAD_GRAYSCALE)
    image9 = cv2.imread('pic.9.png', cv2.IMREAD_GRAYSCALE)
    image10 = cv2.imread('cameraman.tif', cv2.IMREAD_GRAYSCALE)
    image11 = cv2.imread('rice.png', cv2.IMREAD_GRAYSCALE)
    image12 = cv2.imread('pic.10.png', cv2.IMREAD_GRAYSCALE)

    # Apply the dilate function to image1
    dilated_image1 = dilate(image1, kernel_size=3, iterations=1)
    cv2.imwrite('pic.1_dilate.jpg', dilated_image1)

    # Apply the erode function to image2
    eroded_image2 = erode(image2, kernel_size=3, iterations=1)
    cv2.imwrite('pic.2_erode.jpg', eroded_image2)
    
    # Apply the open function to image3
    opened_image3 = mopen(image3, kernel_size=3)
    cv2.imwrite('pic.3_open.jpg', opened_image3)

    # Apply the close function to image3
    closed_image3 = mclose(image3, kernel_size=3)
    cv2.imwrite('pic.3_close.jpg', closed_image3)
    
    # Apply the thin function to image3
    thinned_image3 = thin(image3)
    cv2.imwrite('pic.3_thin.jpg', thinned_image3)
    
    # Apply the skeletonize function to image4
    skeletonized_image4 = skeletonize(image4)
    cv2.imwrite('pic.4_skeletonize.jpg', skeletonized_image4)
    
    # Apply the select_cohesion_components function to image5
    _, cohesion_components = select_cohesion_components(image5)
    cv2.imwrite('pic.5_cohesion_components.jpg', cohesion_components)
    
    # Apply the morphological_reconstruction function to image6a and image6b
    reconstructed_image6 = morphological_reconstruction(image6a, image6b)
    cv2.imwrite('pic.6_reconstruct.jpg', reconstructed_image6)

    # Apply the morphological_reconstruction function to marker and mask
    reconstructed_image7 = morphological_reconstruction(image7, image7)
    cv2.imwrite('pic.7_reconstruct.jpg', reconstructed_image7)

    # Apply the halftone_dilate function to image8
    halftone_dilated_image8 = halftone_dilate(image8, kernel_size=3, iterations=1)
    cv2.imwrite('pic.8_halftone_dilate.jpg', halftone_dilated_image8)

    # Apply the halftone_erode function to image8
    halftone_eroded_image8 = halftone_erode(image8, kernel_size=3, iterations=1)
    cv2.imwrite('pic.8_halftone_erode.jpg', halftone_eroded_image8)

    # Apply the halftone_open function to image9
    halftone_opened_image9 = halftone_open(image9, kernel_size=3)
    cv2.imwrite('pic.9_halftone_open.jpg', halftone_opened_image9)

    # Apply the halftone_close function to image9
    halftone_closed_image9 = halftone_close(image9, kernel_size=3)
    cv2.imwrite('pic.9_halftone_close.jpg', halftone_closed_image9)

    # Apply the morphological_gradient function to cameraman
    morphological_gradient_cameraman = morphological_gradient(image10)
    cv2.imwrite('cameraman_morphological_gradient.jpg', morphological_gradient_cameraman)

    # Apply the top_hat function to rice
    top_hat_rice = top_hat(image11)
    cv2.imwrite('rice_top_hat.jpg', top_hat_rice)

    # Apply the morphological_halftone_reconstruction function to pic.10
    morphological_halftone_reconstructed_image12 = morphological_halftone_reconstruction(image12, image12)
    cv2.imwrite('pic.10_morphological_halftone_reconstruct.jpg', morphological_halftone_reconstructed_image12)
