import numpy as np

def graythresh(image):
	'''Implements global image threshold using Otsu's method'''

	nbins = 256
	#p, _ = np.histogram(image, bins = nbins, range = [0, nbins - 1], density = True)
	p, _ = np.histogram(image, bins = nbins, range = [0, nbins - 1])
	p = p / (image.shape[0] * image.shape[1])
	
	omega = np.cumsum(p)
	mu = np.cumsum(p * np.arange(1, nbins + 1))
	mu_t = mu[-1]	# Last element
	
	sigma_b2 = (mu_t * omega - mu) ** 2 / (omega * (1 - omega) + np.finfo(omega.dtype).eps)

	maxval = np.nanmax(sigma_b2)
	if (np.isnan(maxval)):
		level = 0
	else:
		i = np.mean(np.nonzero(sigma_b2 == maxval))
		level = i / (nbins - 1)
	
	return level