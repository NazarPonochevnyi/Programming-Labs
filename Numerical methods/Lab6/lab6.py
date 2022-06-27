"""
Interpolation

"""

import math
import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt


# ------------ Input ------------


def f(x):
    return x**2 * math.cos(x)


A, B = -math.pi / 2, math.pi


# ------------ Code ------------


def chebyshev_nodes(n, a, b):
    nodes = []
    for k in range(1, n + 1):
        nodes.append((0.5 * (a + b)) + ((0.5 * (b - a)) * math.cos((((2 * k) - 1) * math.pi) / (2 * n))))
    return nodes


def build_lagrange_polynom(X, y):
    x = sp.Symbol('x')
    L = 0
    for i in range(len(y)):
      nominator = y[i]
      for j in range(len(y)):
        if j != i:
          nominator *= (x - X[j])
      denominator = 1
      for j in range(len(y)):
        if j != i:
          denominator *= (X[i] - X[j])
      L += (nominator / denominator)
    return sp.simplify(L)


def build_cubic_splines(x0, x, y):
    x = np.asfarray(x)
    y = np.asfarray(y)
    size = len(x)
    xdiff = np.diff(x)
    ydiff = np.diff(y)
    Li = np.empty(size)
    Li_1 = np.empty(size-1)
    z = np.empty(size)
    Li[0] = math.sqrt(2*xdiff[0])
    Li_1[0] = 0.0
    B0 = 0.0
    z[0] = B0 / Li[0]

    for i in range(1, size-1, 1):
        Li_1[i] = xdiff[i-1] / Li[i-1]
        Li[i] = math.sqrt(2*(xdiff[i-1]+xdiff[i]) - Li_1[i-1] * Li_1[i-1])
        Bi = 6*(ydiff[i]/xdiff[i] - ydiff[i-1]/xdiff[i-1])
        z[i] = (Bi - Li_1[i-1]*z[i-1])/Li[i]

    i = size - 1
    Li_1[i-1] = xdiff[-1] / Li[i-1]
    Li[i] = math.sqrt(2*xdiff[-1] - Li_1[i-1] * Li_1[i-1])
    Bi = 0.0
    z[i] = (Bi - Li_1[i-1]*z[i-1])/Li[i]

    i = size-1
    z[i] = z[i] / Li[i]
    for i in range(size-2, -1, -1):
        z[i] = (z[i] - Li_1[i-1]*z[i+1])/Li[i]

    index = x.searchsorted(x0)
    np.clip(index, 1, size-1, index)
    xi1, xi0 = x[index], x[index-1]
    yi1, yi0 = y[index], y[index-1]
    zi1, zi0 = z[index], z[index-1]
    hi1 = xi1 - xi0

    f0 = zi0/(6*hi1)*(xi1-x0)**3 + \
         zi1/(6*hi1)*(x0-xi0)**3 + \
         (yi1/hi1 - zi1*hi1/6)*(x0-xi0) + \
         (yi0/hi1 - zi0*hi1/6)*(xi1-x0)
    return f0


def main():
    X = np.array(sorted(chebyshev_nodes(10, A, B)))
    print(f"Chebyshev's nodes (X):\n{X}")

    Y = np.array([f(x) for x in X])
    df = pd.DataFrame({'X': X, 'Y': Y})
    print(f"\nTable:\n{df}")
    
    x = sp.Symbol('x')
    L = build_lagrange_polynom(X, Y)
    print(f"\nLagrange's polynom:\n{L}")
    
    ls = np.linspace(A - 1, B + 1, 100)
    ls_Y_true = np.array([f(i) for i in ls])
    ls_Y_L = np.array([L.subs(x, i) for i in ls])
    r = max(np.abs(ls_Y_true - ls_Y_L))
    print(f"Max absolute error of the Lagrange's polynom: {round(r, 4)}")


    plt.scatter(X, Y, color="red")
    plt.plot(ls, ls_Y_true, color="green")
    plt.plot(ls, ls_Y_L, linestyle='--')
    plt.show()

    ls_Y_S = build_cubic_splines(ls, X, Y)
    r = max(np.abs(ls_Y_true - ls_Y_S))
    print(f"\nMax absolute error of the Cubic splines: {round(r, 4)}")

    plt.scatter(X, Y, color="red")
    plt.plot(ls, ls_Y_true, color="green")
    plt.plot(ls, ls_Y_S, linestyle='--')
    plt.show()


if __name__ == "__main__":
    main()
