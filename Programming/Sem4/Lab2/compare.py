# Comparing sort algorithms

from time import time
from random import randint

from insertion_sort import insertion_sort
from quick_sort import quick_sort

import sys
sys.setrecursionlimit(10000)

# generate datasets
INF = 2**64
test100 = [randint(-INF, INF) for _ in range(100)]
test1000 = [randint(-INF, INF) for _ in range(1000)]
test10000 = [randint(-INF, INF) for _ in range(10000)]

# true answers
sorted_test100 = sorted(test100)
sorted_test1000 = sorted(test1000)
sorted_test10000 = sorted(test10000)


# analyse function
def analyse(func, data, answer, number, repeat_num=100, reset=False):
    start_time = time()
    func_answer = func(data.copy())
    for _ in range(repeat_num - 1):
        func(data.copy())
    exec_time = (time() - start_time)
    coef = 1 if not reset else repeat_num
    print(f"-- ({func.__name__}) Test on {number} items --\n"
          f"Values: {func_answer == answer}\n"
          f"Number of copies: {func.count_copies / coef}\n"
          f"Number of comparisons: {func.count_comparisons / coef}\n"
          f"Execution time: {round(exec_time, 2)}\n")


# test on 100 items
analyse(insertion_sort, test100,
        sorted_test100, 100, repeat_num=5000)
analyse(quick_sort, test100,
        sorted_test100, 100, repeat_num=5000, reset=True)

# test on 1000 items
analyse(insertion_sort, test1000,
        sorted_test1000, 1000, repeat_num=100)
analyse(quick_sort, test1000,
        sorted_test1000, 1000, repeat_num=100, reset=True)

# test on 10000 items
analyse(insertion_sort, test10000,
        sorted_test10000, 10000, repeat_num=1)
analyse(quick_sort, test10000,
        sorted_test10000, 10000, repeat_num=1, reset=True)
