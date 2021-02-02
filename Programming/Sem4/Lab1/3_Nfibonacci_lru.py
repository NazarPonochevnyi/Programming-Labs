# Find Nth Fibonacci sequence using recursion and LRU cache

from functools import lru_cache, wraps


def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count_calls += 1
        return func(*args, **kwargs)
    wrapper.count_calls = 0
    return wrapper


@count_calls
@lru_cache()
def fibonacci(n):
    if n in (0, 1):
        return 1
    return fibonacci(n - 2) + fibonacci(n - 1)


print(", ".join(map(str, map(fibonacci, range(0, 10)))))
print(fibonacci.count_calls)
