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
