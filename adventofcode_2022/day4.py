import os
import string
import numpy as np
from adventofcode_2022.helper import DPATH


def convert_to_range(input):
    first_pair, second_pair = input.split(',')
    first_set = convert_to_set(*first_pair.split('-'))
    second_set = convert_to_set(*second_pair.split('-'))
    smallest_set, largest_set = sorted([first_set, second_set], key=lambda x: len(x))
    return smallest_set, largest_set


def convert_to_set(lower, upper):
    lower = int(lower)
    upper = int(upper)
    return set(range(lower, upper+1))


def check_overlap(a, b):
    n_difference_a_b = len(a.difference(b))
    n_difference_b_a = len(b.difference(a))
    if (n_difference_b_a == 0) or (n_difference_a_b == 0):
        return True
    else:
        return False


def check_overlap_part_2(a, b):
    n_intersect = len(a.intersection(b))
    if (n_intersect > 0):
        return True
    else:
        return False


dfile = os.path.join(DPATH, 'day4.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x.strip() for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if len(x)]

total_overlap = sum([check_overlap(*convert_to_range(x)) for x in puzzle_input])

total_overlap_part2 = sum([check_overlap_part_2(*convert_to_range(x)) for x in puzzle_input])
