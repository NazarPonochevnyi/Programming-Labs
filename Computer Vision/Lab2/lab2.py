import time
import numpy as np
from imageio import imread
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
from dftfilter import lp_filter, hp_filter, filter, freqz2


# Load the images
f = imread('pic1.jpg')
f2 = imread('pic2.jpg')
PQ = np.shape(f)
PQ2 = np.shape(f2)


# Generate a low-pass filter with an ideal filter
H_lp_ideal = lp_filter('ideal', PQ, 40)

# Generate a low-pass filter with a Butterworth filter
H_lp_btw = lp_filter('btw', PQ, 40, 4)

# Generate a low-pass filter with a Gaussian filter
H_lp_gauss = lp_filter('gaussian', PQ, 40)

# Generate a high-pass filter with an ideal filter
H_hp_ideal = hp_filter('ideal', PQ, 40)

# Generate a high-pass filter with a Butterworth filter
H_hp_btw = hp_filter('btw', PQ, 40, 4)

# Generate a high-pass filter with a Gaussian filter
H_hp_gauss = hp_filter('gaussian', PQ, 40)

# Generate a high-pass filter with a Laplacian filter
H_hp_laplacian = hp_filter('laplacian', PQ)

# Generate a Sobel filter
K_sobel_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
H_sobel_x = freqz2(K_sobel_x, *PQ2)


# Perform low-pass filtering with an ideal filter
g_lp_ideal = filter(f, H_lp_ideal)

# Perform low-pass filtering with a Butterworth filter
g_lp_btw = filter(f, H_lp_btw)

# Perform low-pass filtering with a Gaussian filter
g_lp_gauss = filter(f, H_lp_gauss)

# Perform high-pass filtering with an ideal filter
g_hp_ideal = filter(f, H_hp_ideal)

# Perform high-pass filtering with a Butterworth filter
g_hp_btw = filter(f, H_hp_btw)

# Perform high-pass filtering with a Gaussian filter
g_hp_gauss = filter(f, H_hp_gauss)

# Perform high-pass filtering with a Laplacian filter
g_hp_laplacian = filter(f, H_hp_laplacian)

# Perform Sobel x filtering in the spatial domain
start_time = time.time()
for _ in range(1000):
    g_sobel_x_s = convolve2d(f2, K_sobel_x)
print(f"Sobel x filtering in the spatial domain time: {round(time.time() - start_time, 2)} s")

# Perform Sobel x filtering in the freq domain
start_time = time.time()
for _ in range(1000):
    g_sobel_x_f = filter(f2, H_sobel_x)
print(f"Sobel x filtering in the freq domain: {round(time.time() - start_time, 2)} s")


# Display the original and filtered images
plt.figure()
plt.subplot(241)
plt.imshow(f, cmap='gray')
plt.title('Image')
plt.axis('off')
plt.subplot(242)
plt.imshow(g_lp_ideal, cmap='gray')
plt.title('LP Ideal')
plt.axis('off')
plt.subplot(243)
plt.imshow(g_lp_btw, cmap='gray')
plt.title('LP Butterworth')
plt.axis('off')
plt.subplot(244)
plt.imshow(g_lp_gauss, cmap='gray')
plt.title('LP Gaussian')
plt.axis('off')
plt.subplot(245)
plt.imshow(g_hp_ideal, cmap='gray')
plt.title('HP Ideal')
plt.axis('off')
plt.subplot(246)
plt.imshow(g_hp_btw, cmap='gray')
plt.title('HP Butterworth')
plt.axis('off')
plt.subplot(247)
plt.imshow(g_hp_gauss, cmap='gray')
plt.title('HP Gaussian')
plt.axis('off')
plt.subplot(248)
plt.imshow(g_hp_laplacian, cmap='gray')
plt.title('HP Laplacian')
plt.axis('off')
plt.figure()
plt.subplot(131)
plt.imshow(f2, cmap='gray')
plt.title('Image 2')
plt.axis('off')
plt.subplot(132)
plt.imshow(g_sobel_x_s, cmap='gray')
plt.title('Sobel X (Spat)')
plt.axis('off')
plt.subplot(133)
plt.imshow(g_sobel_x_f, cmap='gray')
plt.title('Sobel X (Freq)')
plt.axis('off')
plt.show()
