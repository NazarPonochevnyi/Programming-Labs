import numpy as np
from scipy.fftpack import fft2, ifft2
from imageio import imread
import matplotlib.pyplot as plt

# Import functions from the script provided in the previous response
from dftfilter import paddedsize
from dftfilter import dftuv
from dftfilter import lp_filter
from dftfilter import hp_filter

# Load the image
f = imread('pic1.jpg')
f = np.array(f)

# Get expansion parameters for zero-padding
PQ = paddedsize(f)

# Compute the Fourier transform of the image with expansion
f = np.expand_dims(f, axis=-1)
F = fft2(f, PQ[0], PQ[1])

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

# Perform low-pass filtering with an ideal filter
G_lp_ideal = H_lp_ideal * F
g_lp_ideal = np.real(ifft2(G_lp_ideal))
g_lp_ideal = g_lp_ideal[:f.shape[0], :f.shape[1]]

# Perform low-pass filtering with a Butterworth filter
G_lp_btw = H_lp_btw * F
g_lp_btw = np.real(ifft2(G_lp_btw))
g_lp_btw = g_lp_btw[:f.shape[0], :f.shape[1]]

# Perform low-pass filtering with a Gaussian filter
G_lp_gauss = H_lp_gauss * F
g_lp_gauss = np.real(ifft2(G_lp_gauss))
g_lp_gauss = g_lp_gauss[:f.shape[0], :f.shape[1]]

# Perform high-pass filtering with an ideal filter
G_hp_ideal = H_hp_ideal * F
g_hp_ideal = np.real(ifft2(G_hp_ideal))
g_hp_ideal = g_hp_ideal[:f.shape[0], :f.shape[1]]

# Perform high-pass filtering with a Butterworth filter
G_hp_btw = H_hp_btw * F
g_hp_btw = np.real(ifft2(G_hp_btw))
g_hp_btw = g_hp_btw[:f.shape[0], :f.shape[1]]

# Perform high-pass filtering with a Gaussian filter
G_hp_gauss = H_hp_gauss * F
g_hp_gauss = np.real(ifft2(G_hp_gauss))
g_hp_gauss = g_hp_gauss[:f.shape[0], :f.shape[1]]

# Perform high-pass filtering with a Laplacian filter
G_hp_laplacian = H_hp_laplacian * F
g_hp_laplacian = np.real(ifft2(G_hp_laplacian))
g_hp_laplacian = g_hp_laplacian[:f.shape[0], :f.shape[1]]

# Load the second image
f2 = imread('pic2.jpg')

# Compute the Fourier transform of the second image
F2 = fft2(f2)

# Generate a low-pass filter with an ideal filter
H2_lp_ideal = lp_filter('ideal', F2.shape, 40)

# Perform low-pass filtering with an ideal filter in the frequency domain
G2_lp_ideal = H2_lp_ideal * F2
g2_lp_ideal = np.real(ifft2(G2_lp_ideal))

# Perform low-pass filtering with an ideal filter in the spatial domain
h2_lp_ideal = lp_filter('ideal', f2.shape, 40)
g2_lp_ideal_spatial = np.real(ifft2(fft2(f2) * h2_lp_ideal))

# Display the original and filtered images
plt.figure()
plt.subplot(231)
plt.imshow(f, cmap='gray')
plt.title('Original image')
plt.axis('off')
plt.subplot(232)
plt.imshow(g_lp_ideal, cmap='gray')
plt.title('Low-pass filtering with an ideal filter')
plt.axis('off')
plt.subplot(233)
plt.imshow(g_lp_btw, cmap='gray')
plt.title('Low-pass filtering with a Butterworth filter')
plt.axis('off')
plt.subplot(234)
plt.imshow(g_lp_gauss, cmap='gray')
plt.title('Low-pass filtering with a Gaussian filter')
plt.axis('off')
plt.subplot(235)
plt.imshow(g_hp_ideal, cmap='gray')
plt.title('High-pass filtering with an ideal filter')
plt.axis('off')
plt.subplot(236)
plt.imshow(g_hp_btw, cmap='gray')
plt.title('High-pass filtering with a Butterworth filter')
plt.axis('off')

plt.figure()
plt.subplot(221)
plt.imshow(g_hp_gauss, cmap='gray')
plt.title('High-pass filtering with a Gaussian filter')
plt.axis('off')
plt.subplot(222)
plt.imshow(g_hp_laplacian, cmap='gray')
plt.title('High-pass filtering with a Laplacian filter')
plt.axis('off')
plt.subplot(223)
plt.imshow(f2, cmap='gray')
plt.title('Original image')
plt.axis('off')
plt.subplot(224)
plt.imshow(g2_lp_ideal, cmap='gray')
plt.title('Low-pass filtering with an ideal filter in the frequency')
