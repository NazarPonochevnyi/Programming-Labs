import cv2
import numpy as np

def process_image(image):
  # Randomly apply affine transformation to image
  rows, cols, _ = image.shape
  pts1 = np.float32([[50,50],[200,50],[50,200]])
  pts2 = np.float32([[10,100],[200,50],[100,250]])
  M = cv2.getAffineTransform(pts1,pts2)
  image = cv2.warpAffine(image, M, (cols, rows))

  # Save region of interest (ROI) from original image
  roi = image[50:200, 50:200]

  # Perform template matching to find ROI in transformed image
  res = cv2.matchTemplate(image, roi, cv2.TM_CCOEFF_NORMED)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

  # Draw bounding box around matched region
  top_left = max_loc
  bottom_right = (top_left[0] + 150, top_left[1] + 150)
  cv2.rectangle(image, top_left, bottom_right, (0,255,0), 2)

  return image

import cv2

# Load image
image = cv2.imread("cameraman.tif")

# Process image
result = process_image(image)

# Save result
cv2.imwrite("result.jpg", result)



