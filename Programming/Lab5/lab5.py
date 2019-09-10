"""
2. Створіть програму, що підраховує частоти входження слів в текстовому файлі. 
"""

import string
from collections import Counter

input_file = 'text.txt'

def count_words(words, sort=False):
    words_count = {}
    for word in words:
        if word in words_count.keys():
            words_count[word] += 1
        else:
            words_count[word] = 1
    if sort:
        words_count = [(k, words_count[k]) for k in sorted(words_count, \
            key=words_count.get, reverse=True)]
    return words_count

words = []
with open(input_file, 'r', encoding='utf-8') as f:
    for word in f.read().split():
        word = word.strip().lower()
        for item in string.punctuation + string.digits:
            word = word.replace(item, '')
        if word: words.append(word)

words_count = Counter(words).most_common() # або можна використати мою функцію: count_words(words, sort=True)

print('\nAmount of words: {}\n\nWords stats:'.format(len(words)))
for word, amount in words_count:
    print('\t{} -> {}'.format(word, amount))
