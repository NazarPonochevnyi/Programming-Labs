import cv2
import numpy as np
import matplotlib.pyplot as plt


def plot_hist(images):
    for img in images:
        plt.hist(img.ravel(), 256, (0, 256))
    plt.show()

def negative(image_path):
    img = cv2.imread(image_path)
    negative_img = 255 - img
    cv2.imwrite(f"{image_path.split('.')[0]}_negative.jpg", negative_img)

def logarithmic(image_path):
    img = cv2.imread(image_path)
    c = 10
    log_img = c * np.log(1 + img)
    log_img = log_img.astype(np.uint8)
    cv2.imwrite(f"{image_path.split('.')[0]}_logarithmic.jpg", log_img)

def power(image_path):
    img = cv2.imread(image_path)
    c = 2
    gamma = 1.5
    power_img = c * img**gamma
    cv2.imwrite(f"{image_path.split('.')[0]}_power.jpg", power_img)

def contrast_stretch(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    stretched_img = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    cv2.imwrite(f"{image_path.split('.')[0]}_stretched.jpg", stretched_img)
    plot_hist([gray, stretched_img])

def histogram_equalization(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hist_eq_img = cv2.equalizeHist(gray)
    hist_eq_img = hist_eq_img.astype(np.uint8)
    cv2.imwrite(f"{image_path.split('.')[0]}_hist_eq.jpg", hist_eq_img)
    plot_hist([gray, hist_eq_img])

def averaging_filter(image_path):
    img = cv2.imread(image_path)
    smooth_img = cv2.blur(img, (3, 3))
    cv2.imwrite(f"{image_path.split('.')[0]}_smooth.jpg", smooth_img)

def laplace_sharpening(image_path):
    img = cv2.imread(image_path)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharp_img = cv2.filter2D(img, -1, kernel)
    cv2.imwrite(f"{image_path.split('.')[0]}_sharp.jpg", sharp_img)

def gradient(image_path):
    img = cv2.imread(image_path)
    kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    grad_x_img = cv2.filter2D(img, -1, kernel)
    kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    grad_y_img = cv2.filter2D(img, -1, kernel)
    cv2.imwrite(f"{image_path.split('.')[0]}_grad_x.jpg", grad_x_img)
    cv2.imwrite(f"{image_path.split('.')[0]}_grad_y.jpg", grad_y_img)

def median_filter(image_path):
    img = cv2.imread(image_path)
    median_img = cv2.medianBlur(img, 3)
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
