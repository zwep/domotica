import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def day1(x_input):
    return None


def day2(x_input):
    return None


DAY = "9"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)


# Determine differences
def get_diff(int_list, memory=None):
    if memory is None:
        memory = []
    if all([x == 0 for x in int_list]):
        return memory

    temp_difference = [iy - ix for iy, ix in zip(int_list[1:], int_list[:-1])]
    memory.append(temp_difference)
    return get_diff(temp_difference, memory=memory)

s = 0
for i_line in puzzle_input:
    int_list = helper.int_str2list(i_line)
    z = get_diff(int_list)
    z.append(int_list)
    test_s = sum([x[-1] for x in z])
    s += test_s


s = 0
for i_line in puzzle_input:
    int_list = helper.int_str2list(i_line)
    z = get_diff(int_list)
    z.insert(0, int_list)
    test_s1 = sum([x[0] for x in z[::2]])
    test_s2 = sum([x[0] for x in z[1::2]])
    s += (test_s1 - test_s2)

s
