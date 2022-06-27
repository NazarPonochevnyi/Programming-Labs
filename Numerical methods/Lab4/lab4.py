"""
Finding all eigenvalues

"""

# ------------ Input ------------


import numpy as np
import sympy as sp


A = np.array([[6.26, 1.10, 0.98, 1.25],
              [1.10, 4.16, 1., 0.16],
              [0.98, 1., 5.44, 2.12],
              [1.25, 0.16, 2.12, 6.]])


# ------------ Code ------------


def danilevsky_method(f):
    for i in range(len(f) - 1):
        m = np.identity(len(f))
        m[len(f) - 2 - i][:] = f[len(f) - 1 - i][:]
        print(f"\nM{i + 1}:\n{m}")
        print(f"M^(-1){i + 1}:\n{np.linalg.inv(m)}")
        f = np.dot(m, f)
        f = np.dot(f, np.linalg.inv(m))
    return f


def equation_solve(p):
    x = sp.Symbol('x')
    e = x**4 - p[0] * x**3 - p[1] * x**2 - p[2] * x - p[3]
    return e, sp.solve(e, x)


def main():
    print(f"A:\n{A}")
    f = danilevsky_method(A)
    e, lambdas = equation_solve(f[0][:])
    print(f"\nF:\n{f}")
    print(f"\nCharacteristic Equation:\n{e} = 0")
    print(f"\nEigenvalues:\n{lambdas}")
    print(f"\nNumPy Eigenvalues:\n{list(np.linalg.eig(A)[0])}")


if __name__ == "__main__":
    main()
