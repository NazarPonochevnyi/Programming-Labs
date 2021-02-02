# Quick Sort

from random import randint


def quick_sort(array):
    lenght = len(array)
    if lenght <= 1:
        return array
    less = []
    equal = []
    greater = []
    p = array[randint(0, lenght - 1)]
    for item in array:
        quick_sort.count_comparisons += 1
        if item < p:
            less.append(item)
        elif item == p:
            equal.append(item)
        else:
            greater.append(item)
        quick_sort.count_copies += 1
    return quick_sort(less) + equal + quick_sort(greater)


quick_sort.count_copies = 0
quick_sort.count_comparisons = 0

if __name__ == "__main__":
    arr = [5, 7, 1, 3, 4]
    quick_sort(arr)
    print(arr)
    print(quick_sort.count_copies)
    print(quick_sort.count_comparisons)
