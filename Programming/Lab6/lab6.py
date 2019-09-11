"""
38. Скільки літер "в" у слові стоїть на парних місцях?
"""

word = input("Input word: ").strip()

amount = 0
for i in range(1, len(word), 2):
    if word[i] == 'в':
        amount += 1

print('Amount of "в" in word:', amount)
