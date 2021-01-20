import numpy as np
import os
import sys

with open("adventofcode_2020/day10_numbers.txt", "r") as f:
    A = [int(x) for x in f.read().splitlines()]

list_A = sorted(A)
list_difference = [x - y for x, y in zip(list_A[1:], list_A[:-1])]
jolt_1 = sum([x == 1 for x in list_difference]) + 1
jolt_3 = sum([x == 3 for x in list_difference]) + 1

jolt_3 * jolt_1


# Day2


with open("adventofcode_2020/day10_numbers.txt", "r") as f:
    A = [int(x) for x in f.read().splitlines()]

list_A = sorted(A)
list_A = [0] + list_A + [(list_A[-1] + 3)]
occurence_A = [0] * (len(list_A) - 1)
for i_pos, i_jolt in enumerate(list_A[:-1]):
    max_step = 0
    for i in [1, 2, 3]:
        if i_jolt + i in list_A[(i_pos+1):]:
            # occurence_A[i_pos] += i
            max_step = i

s = 1
for i in occurence_A:
    s = s * i
