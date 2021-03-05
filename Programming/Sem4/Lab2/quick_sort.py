# Quick Sort

from random import randint


def quick_sort(array, left=0, right=None):
    if right is None:
        right = len(array) - 1
    i = left
    j = right
    pivot = array[randint(left, right)]
    while i <= j:
        quick_sort.count_comparisons += 2
        while array[i] < pivot:
            i += 1
            quick_sort.count_comparisons += 1
        while array[j] > pivot:
            j -= 1
            quick_sort.count_comparisons += 1
        if i <= j:
            array[i], array[j] = array[j], array[i]
            i += 1
            j -= 1
            quick_sort.count_copies += 2
    if left < j:
        quick_sort(array, left, j)
    if i < right:
        quick_sort(array, i, right)


quick_sort.count_copies = 0
quick_sort.count_comparisons = 0

if __name__ == "__main__":
    arr = [5, 7, 1, 3, 4]
    quick_sort(arr)
    print(arr)
    print(quick_sort.count_copies)
    print(quick_sort.count_comparisons)
