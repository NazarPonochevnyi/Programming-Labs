import re
import time
import numpy as np
from hmmlearn import hmm


with open("kobzar.txt", "r", encoding='utf8') as file:
    rtext = file.read()

rtext = rtext.lower()
rtext = re.sub(r'[^\w\s]|\d', '', rtext)
rtext = rtext.replace('\n', ' ')
chars = sorted(set(rtext))
n_characters = len(chars)
text = np.atleast_2d([chars.index(char) for char in rtext]).T
print(f"К-ть символів: {len(rtext)}\nСимволи ({n_characters}): {chars}")

for n_states in range(2, 5):
    print(f"\n\nК-ть станів: {n_states}")
    initial_distribution = np.array([1/n_states] * n_states)
    transition_matrix = np.ones((n_states, n_states)) / n_states

    model = hmm.CategoricalHMM(n_components=n_states, init_params="", n_iter=1000)
    model.startprob_ = initial_distribution
    model.transmat_ = transition_matrix
    start_time = time.time()
    model.fit(text)
    print(f"\nНавчання зайняло {round(time.time() - start_time, 2)} сек")

    print(f"\nA: {model.transmat_}\nμ: {model.startprob_}")
    preds = []
    for i, char in enumerate(chars):
        prob = model.emissionprob_[:, i]
        state = np.argmax(prob)
        preds.append((char, state))
    print(f"\nРезультат: {sorted(preds, key=lambda x: x[1])}")
