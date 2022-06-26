"""
Iteratively solving a system of equations

"""

# ------------ Input ------------


import numpy as np


A = np.array([[0.5644, 0.1296, 0.3948, 0.],
              [0.1296, 0.8064, 0.2232, 0.],
              [0.0054, -0.0364, 0.8218, -0.59],
              [0.005296, 0.289664, -0.237968, 1.]])

b = np.array([-0.294, 0.104, -0.029, 1.24104]).reshape(-1, 1)

e = 10**-4


# ------------ Code ------------


def simple_iteration_method(C, x, d):
    return C.dot(x) + d


def main():
    C = np.zeros_like(A)
    for i in range(len(C)):
        for j in range(len(C)):
            if i != j:
                C[i, j] = -A[i, j] / A[i, i]
    d = np.zeros_like(b)
    for i in range(len(d)):
        d[i, 0] = b[i, 0] / A[i, i]
    x = np.ones_like(b)
    q = max(np.sum(np.abs(C), axis=1)) + 0.01
    print(f"C:\n{C}")
    print(f"d:\n{d}")
    print(f"x0:\n{x}")
    print(f"q:\n{q}")

    i = 1
    x_new = simple_iteration_method(C, x, d)
    r = np.sum(np.abs(b - A.dot(x_new)))
    criteria = (1 / (1 - q)) * max(np.abs(x_new - x))
    print(f"\nIteration #{i}\nx:\n{x_new}")
    print(f"r: {r}")
    print(f"criteria: {criteria}")
    while criteria >= e:
        x = x_new
        i += 1
        x_new = simple_iteration_method(C, x, d)
        r = np.sum(np.abs(b - A.dot(x_new)))
        criteria = (1 / (1 - q)) * max(np.abs(x_new - x))
        print(f"\nIteration #{i}\nx:\n{x_new}")
        print(f"r: {r}")
        print(f"criteria: {criteria}")


if __name__ == "__main__":
    main()
