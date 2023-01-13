import re
import time
import numpy as np
from hmmlearn import hmm


def viterbi(y, A, B, Pi=None):
    K = A.shape[0]
    Pi = Pi if Pi is not None else np.full(K, 1 / K)
    T = len(y)
    T1 = np.empty((K, T), 'd')
    T2 = np.empty((K, T), 'B')

    T1[:, 0] = Pi * B[:, y[0]]
    T2[:, 0] = 0

    for i in range(1, T):
        T1[:, i] = np.max(T1[:, i - 1] * A.T * B[np.newaxis, :, y[i]].T, 1)
        T2[:, i] = np.argmax(T1[:, i - 1] * A.T, 1)

    x = np.empty(T, 'B')
    x[-1] = np.argmax(T1[:, T - 1])
    for i in reversed(range(1, T)):
        x[i - 1] = T2[x[i], i]
    return x, T1, T2


chars = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
n_characters = len(chars)
with open("secret_kobzar.txt", "r", encoding='utf8') as file:
    raw_secret_text = file.read()
secret_text = np.atleast_2d([chars.index(char) for char in raw_secret_text]).T
print(f"К-ть зашифрованих символів: {len(raw_secret_text)}\nСимволи ({n_characters}): {chars}")
with open("extra_kobzar.txt", "r", encoding='utf8') as file:
    raw_extra_text = file.read()
extra_text = [chars.index(char) for char in raw_extra_text]
print(f"К-ть додаткових символів: {len(raw_extra_text)}\nСимволи ({n_characters}): {chars}")

n_states = n_characters
A = np.zeros((n_characters, n_characters))
for i in range(len(extra_text) - 1):
    x, y = extra_text[i], extra_text[i + 1]
    A[x, y] += 1
A += 5
A = A / A.sum(axis=1, keepdims=True)
w, v = np.linalg.eig(A.T)
stationary = v[:, np.argmax(w)].real
stationary = stationary / stationary.sum()
emission_matrix = np.ones((n_states, n_characters)) / n_characters

model = hmm.CategoricalHMM(n_components=n_states, init_params="", n_iter=200)
model.startprob_ = stationary
model.transmat_ = A
model.emissionprob_ = emission_matrix
start_time = time.time()
model.fit(secret_text[:1000])
print(f"\nНавчання зайняло {round(time.time() - start_time, 2)} сек")

print(f"\nA: {model.transmat_}\nB: {model.emissionprob_}\nμ: {model.startprob_}")
preds = []
for i, char in enumerate(chars):
    prob = model.emissionprob_[:, i]
    state = np.argmax(prob)
    preds.append((char, chars[state], i - state))
print(f"\nРезультат: {preds}")

x, _, _ = viterbi(secret_text.squeeze()[:100], model.transmat_, model.emissionprob_, model.startprob_)
decoded_text = ''.join([chars[i] for i in x])
print(f"\nРозшифрований текст: {decoded_text}")
