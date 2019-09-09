"""
2. Нехай дано матрицю, кожний елемент
якої інтерпретується як значення інтенсивності
пікселя деякого зображення. Необхідно знайти
градієнт цього зображення (так званий оператор
Собеля).
"""

import cv2
import random
import numpy as np

image = cv2.imread('./walve.png')
matrix = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
n, m = matrix.shape

g_n, g_m = n - 2, m - 2
G = np.zeros((g_n, g_m))

print('\nMatrix:')
cv2.imshow('Image', image)

for i in range(g_n):
    for j in range(g_m):
        k, l = i + 1, j + 1
        G_x = matrix[k-1][l-1] + 2*matrix[k-1][l] + matrix[k-1][l+1] - matrix[k+1][l-1] - 2*matrix[k+1][l] - matrix[k+1][l+1]
        G_y = matrix[k-1][l-1] + 2*matrix[k][l-1] + matrix[k+1][l-1] - matrix[k-1][l+1] - 2*matrix[k][l+1] - matrix[k+1][l+1]
        G[i][j] = ((G_x ** 2) + (G_y ** 2)) ** 0.5

print('\nGradient:')
G *= (255.0 / G.max())
cv2.imshow('Gradient', G)
cv2.waitKey()