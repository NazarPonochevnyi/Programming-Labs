import numpy as np
import scipy.ndimage.filters as filters

def colorgrad(f, t = 1):
	'''Computes the vector gradient of an RGB image
	   f - image
	   t - threshold in the range [0, 1]
	   Returned values (Vg, A, PPG)
	   VG  - vector gradient
	   A   - angle
	   PPG - per-plane gradient
	'''
	# Using Sobel operator
	h_x = np.array([[-1, 0, 1],
	                [-2, 0, 2],
	                [-1, 0, 1]])
	h_y = h_x.T
	
	# Partial derivatives
	Rx = filters.convolve(f[:, :, 0].astype('float32'), h_x, mode = 'nearest')
	Ry = filters.convolve(f[:, :, 0].astype('float32'), h_y, mode = 'nearest')

	Gx = filters.convolve(f[:, :, 1].astype('float32'), h_x, mode = 'nearest')
	Gy = filters.convolve(f[:, :, 1].astype('float32'), h_y, mode = 'nearest')

	Bx = filters.convolve(f[:, :, 2].astype('float32'), h_x, mode = 'nearest')
	By = filters.convolve(f[:, :, 2].astype('float32'), h_y, mode = 'nearest')
	
	# Parameters of the vector gradient (VG)
	gxx = Rx * Rx + Gx * Gx + Bx * Bx
	gyy = Ry * Ry + Gy * Gy + By * By
	gxy = Rx * Ry + Gx * Gy + Bx * By
	
	# 
	A  = 0.5 * np.arctan2(2 * gxy, gxx - gyy);
	G1 = 0.5 * ((gxx + gyy) + (gxx - gyy) * np.cos(2 * A) + 2 * gxy * np.sin(2 * A))

	A = A + np.pi / 2; # Repeat for angle + pi / 2
	G2 = 0.5 * ((gxx + gyy) + (gxx - gyy) * np.cos(2 * A) + 2 * gxy * np.sin(2 * A))
	
	G1[G1 < 0] = 0
	G2[G2 < 0] = 0
	G1 = np.sqrt(G1)
	G2 = np.sqrt(G2)
	
	VG = np.maximum(G1, G2)
	VG = VG / np.max(VG)
	
	#####
	# Compute per-plane gradients.
	RG = np.sqrt(Rx * Rx + Ry * Ry)
	GG = np.sqrt(Gx * Gx + Gy * Gy)
	BG = np.sqrt(Bx * Bx + By * By)

    # Composite gradient image
	PPG = RG + GG + BG
	PPG = PPG / np.max(PPG)
	
	# Thresholding
	if (t < 1):
		VG[VG < T] = 0
		PPG[PPG < T] = 0
	
	return VG, A, PPG
	