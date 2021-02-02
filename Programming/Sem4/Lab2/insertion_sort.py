# Insertion Sort

def insertion_sort(array):
    insertion_sort.count_copies = 0
    insertion_sort.count_comparisons = 0
    for j in range(1, len(array)):
        key = array[j]
        i = j - 1
        insertion_sort.count_comparisons += 1
        while i >= 0 and array[i] > key:
            array[i + 1] = array[i]
            insertion_sort.count_copies += 1
            i -= 1
        array[i + 1] = key
        insertion_sort.count_copies += 1
    return array


if __name__ == "__main__":
    arr = [5, 7, 1, 3, 4]
    insertion_sort(arr)
    print(arr)
    print(insertion_sort.count_copies)
    print(insertion_sort.count_comparisons)