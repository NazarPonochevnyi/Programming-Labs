"""
2. Нехай дано матрицю, кожний елемент
якої інтерпретується як значення інтенсивності
пікселя деякого зображення. Необхідно знайти
градієнт цього зображення (так званий оператор
Собеля).
"""

import random

n, m = 2000, 2000
g_n, g_m = n - 2, m - 2

matrix = [[random.randint(1, 255) for _ in range(m)] for _ in range(n)]
G = [[0 for _ in range(g_m)] for _ in range(g_n)]

print('\nMatrix:')
for row in matrix:
    print(row)

for i in range(g_n):
    for j in range(g_m):
        k, l = i + 1, j + 1
        G_x = matrix[k-1][l-1] + 2*matrix[k-1][l] + matrix[k-1][l+1] - matrix[k+1][l-1] - 2*matrix[k+1][l] - matrix[k+1][l+1]
        G_y = matrix[k-1][l-1] + 2*matrix[k][l-1] + matrix[k+1][l-1] - matrix[k-1][l+1] - 2*matrix[k][l+1] - matrix[k+1][l+1]
        G[i][j] = ((G_x ** 2) + (G_y ** 2)) ** 0.5

print('\nGradient:')
for row in G:
    print(row)