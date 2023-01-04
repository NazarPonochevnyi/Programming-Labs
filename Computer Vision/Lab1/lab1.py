import cv2
import numpy as np
import matplotlib.pyplot as plt


def plot_hist(images):
    for img in images:
        plt.hist(img.ravel(), 256, (0, 256))
    plt.show()

def negative(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to negative
    negative_img = 255 - img

    # Save the negative image
    cv2.imwrite(f"{image_path.split('.')[0]}_negative.jpg", negative_img)

def logarithmic(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to logarithmic transformation
    c = 10
    log_img = c * np.log(1 + img)

    # Save the logarithmic transformation image
    log_img = log_img.astype(np.uint8)
    cv2.imwrite(f"{image_path.split('.')[0]}_logarithmic.jpg", log_img)

def power(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to power transformation
    c = 2
    gamma = 1.5
    power_img = c * img**gamma

    # Save the power transformation image
    cv2.imwrite(f"{image_path.split('.')[0]}_power.jpg", power_img)

def contrast_stretch(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Stretch the contrast of the image
    stretched_img = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    # Save the stretched image
    cv2.imwrite(f"{image_path.split('.')[0]}_stretched.jpg", stretched_img)

    # Plot hist to check if correct
    plot_hist([gray, stretched_img])

def histogram_equalization(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Equalize the histogram of the grayscale image
    hist_eq_img = cv2.equalizeHist(gray)

    # Save the equalized histogram image
    hist_eq_img = hist_eq_img.astype(np.uint8)
    cv2.imwrite(f"{image_path.split('.')[0]}_hist_eq.jpg", hist_eq_img)

    # Plot hist to check if correct
    plot_hist([gray, hist_eq_img])

def averaging_filter(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Smooth the image using an averaging filter
    smooth_img = cv2.blur(img, (3, 3))

    # Save the smoothed image
    cv2.imwrite(f"{image_path.split('.')[0]}_smooth.jpg", smooth_img)

def laplace_sharpening(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Sharpen the image using a Laplace mask
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharp_img = cv2.filter2D(img, -1, kernel)

    # Save the sharpened image
    cv2.imwrite(f"{image_path.split('.')[0]}_sharp.jpg", sharp_img)

def gradient(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Perform gradient processing in the horizontal direction
    kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    grad_x_img = cv2.filter2D(img, -1, kernel)

    # Perform gradient processing in the vertical direction
    kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    grad_y_img = cv2.filter2D(img, -1, kernel)

    # Save the gradient images
    cv2.imwrite(f"{image_path.split('.')[0]}_grad_x.jpg", grad_x_img)
    cv2.imwrite(f"{image_path.split('.')[0]}_grad_y.jpg", grad_y_img)

def median_filter(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Perform median filtering
    median_img = cv2.medianBlur(img, 3)

    # Save the median filtered image
    cv2.imwrite(f"{image_path.split('.')[0]}_median.jpg", median_img)


if __name__ == "__main__":
    negative("pic1.jpg")
    logarithmic("pic2.jpg")
    power("pic3.jpg")
    contrast_stretch("pic4.jpg")
    histogram_equalization("pic5.jpg")
    averaging_filter("pic6.jpg")
    laplace_sharpening("pic7.jpg")
    gradient("pic8.jpg")
    median_filter("pic9.jpg")
