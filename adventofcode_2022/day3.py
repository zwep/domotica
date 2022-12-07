import os
import string
import numpy as np
from adventofcode_2022.helper import DPATH


def get_overlap(x):
    n_char = len(x) // 2
    x_first = list(x[:n_char])
    x_second = list(x[n_char:])
    return set(x_first).intersection(set(x_second))


def get_score(overlap_list):
    score = 0
    for char in overlap_list:
        if char in string.ascii_lowercase:
            score += 1 + string.ascii_lowercase.index(char)
        if char in string.ascii_uppercase:
            score += 27 + string.ascii_uppercase.index(char)
    return score


dfile = os.path.join(DPATH, 'day3.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x.strip() for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if len(x)]

total_score = 0
for i_knapsack in puzzle_input:
    overlap_set = get_overlap(i_knapsack)
    if len(overlap_set):
        temp_score = get_score(list(overlap_set))
        print(temp_score)
        total_score += temp_score

print(total_score)

# Problem 2
total_score = 0
for i in range(len(puzzle_input)//3):
    x, y, z = map(set, puzzle_input[3*i:3*i+3])
    overlap = x.intersection(y).intersection(z)
    total_score += get_score(overlap)

print(total_score)