import numpy as np

import os

with open('adventofcode_2020/day1_numbers.txt', 'r') as f:
    A = f.readlines()
A = list(map(int, A))


B = sorted(A)
target = 2020
temp = 0
j = i = 0
counter = 0
while temp != target:
    temp = B[i] + B[-(j+1)]
    print(temp, B[i], j)

    counter += 1
    if temp < target:
        i += 1
    if temp > target:
        j += 1

# Part 2
N = len(A)
temp = 0
counter = 0
target = 2020
i_array = list(range(N))
j_array = list(range(N))
k_array = list(range(N))
while temp != target:
    counter += 1
    i = np.random.choice(i_array)
    # print(len(i_array), i)
    index_i = i_array.index(i)
    # i_array.pop(index_i)
    j = np.random.choice(j_array)
    # print(len(j_array), j)
    index_j = j_array.index(j)
    # j_array.pop(index_j)
    k = np.random.choice(k_array)
    # print(len(k_array), k)
    index_k = k_array.index(k)
    # k_array.pop(index_k)
    temp = A[i] + A[j] + A[k]
    # print(temp, end='\n\n')

print(A[i] * A[j] * A[k])