"""
Solving polynoms

"""

# ------------ Input ------------


def f(x):
    return -x**4 + 3 * x**3 - 2 * x + 4


def df(x):
    return -4 * x**3 + 9 * x**2 + 2


INTERVALS = [(-2, 0), (2, 4)]
ACCURACY = 5


# ------------ Code ------------


def bisect(function, derivative, number, a, b, acc, counter=1, debug=True) -> float:
    e = 10**-acc
    mid = (a + b) / 2
    if debug:
        print(f"Iteration: {counter}, Root #{number}: {round(mid, acc)}, Abs. len.: {round(abs(a - b), acc)}")
    while abs(a - b) >= e:
        if function(a) * function(mid) <= 0:
            b = mid
        elif function(mid) * function(b) <= 0:
            a = mid
        mid = (a + b) / 2
        counter += 1
        if debug:
            print(f"Iteration: {counter}, Root #{number}: {round(mid, acc)}, Abs. len.: {round(abs(a - b), acc)}")
    return mid


def secant(function, derivative, number, a, b, acc, counter=1, debug=True) -> float:
    e = 10 ** -acc
    mid = (a + b) / 2
    x, x_prev = mid, mid + 2 * e
    if debug:
        print(f"Iteration: {counter}, Root #{number}: {round(x, acc)}, Abs. change.: {round(abs(x - x_prev), acc)}")
    while abs(x - x_prev) >= e:
        x, x_prev = x - function(x) / (function(x) - function(x_prev)) * (x - x_prev), x
        counter += 1
        if debug:
            print(f"Iteration: {counter}, Root #{number}: {round(x, acc)}, Abs. change.: {round(abs(x - x_prev), acc)}")
    return x


def newton(function, derivative, number, a, b, acc, counter=1, debug=True) -> float:
    e = 10 ** -acc
    mid = (a + b) / 2
    x, x_prev = mid, mid + 2 * e
    if debug:
        print(f"Iteration: {counter}, Root #{number}: {round(x, acc)}, Abs. change.: {round(abs(x - x_prev), acc)}")
    while abs(x - x_prev) >= e:
        x, x_prev = x - function(x) / derivative(x), x
        counter += 1
        if debug:
            print(f"Iteration: {counter}, Root #{number}: {round(x, acc)}, Abs. change.: {round(abs(x - x_prev), acc)}")
    return x


def find_roots(function, derivative, intervals, method, accuracy=5, debug=True) -> list:
    roots = []
    for i, (a, b) in enumerate(intervals):
        root = round(method(function, derivative,
                            i + 1, a, b, accuracy), accuracy)
        roots.append(root)
        if debug:
            print()
    return roots


def main():
    print("\n------------ Bisect method ------------")
    roots = find_roots(f, df, INTERVALS, bisect, ACCURACY, True)
    print("Roots:", roots)

    print("\n------------ Secant method ------------")
    roots = find_roots(f, df, INTERVALS, secant, ACCURACY, True)
    print("Roots:", roots)

    print("\n------------ Newton method ------------")
    roots = find_roots(f, df, INTERVALS, newton, ACCURACY, True)
    print("Roots:", roots)


if __name__ == "__main__":
    main()
