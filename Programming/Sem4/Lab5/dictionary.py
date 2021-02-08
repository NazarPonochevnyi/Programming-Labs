# Create dictionary using binary search tree

import time
import string
from tree import BinaryTree

FILEPATH = "./small_text.txt"

words = set()
words_tree = BinaryTree()
table = str.maketrans('', '', string.punctuation)


def create():
    global words, words_tree
    with open(FILEPATH, 'r', encoding="utf-8") as file:
        for line in file.readlines():
            for line_word in line.strip().split():
                line_word = line_word.strip().lower().translate(table)
                if line_word:
                    words.add(line_word)
    words = list(words)
    for word in words:
        words_tree.insert(word)


def search_file(value, debug=False):
    founded = words.count(value)
    if not founded:
        words.append(value)
        if debug:
            print(f"Word '{value}' added to file")
    else:
        if debug:
            print(f"Word '{value}' founded in file")


def search_tree(value, debug=False):
    founded = words_tree.search(value)
    if not founded:
        words_tree.insert(value)
        if debug:
            print(f"Word '{value}' added to binary tree")
    else:
        if debug:
            print(f"Word '{value}' founded in binary tree")


def remove(value, debug=False):
    # file
    founded = words.count(value)
    if founded:
        words.remove(value)
        if debug:
            print(f"Word '{value}' removed from file")
    else:
        if debug:
            print(f"Word '{value}' not found in file")
    # binary tree
    founded = words_tree.search(value)
    if founded:
        words_tree.remove(value)
        if debug:
            print(f"Word '{value}' removed from binary tree")
    else:
        if debug:
            print(f"Word '{value}' not found in binary tree")


def display():
    print(words)
    words_tree.display()


def main():
    create()
    print(f"List and binary tree with {len(words)} words created")

    print("\nStarting benchmark...")
    start_time = time.time()
    for _ in range(10000):
        search_file('superword')
    duration = time.time() - start_time
    print(f"(file) Search execution time: {round(duration, 3)} s")

    start_time = time.time()
    for _ in range(10000):
        search_tree('superword')
    duration = time.time() - start_time
    print(f"(tree) Search execution time: {round(duration, 3)} s")

    print("\nRemove word:")
    remove('a', debug=True)

    print("\nShow list and binary tree:")
    display()


if __name__ == "__main__":
    main()
