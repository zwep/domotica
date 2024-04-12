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


DAY = "24"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

selected_puzzle = test_puzzle_input

i_line = "19, 13, 30 @ -2, 1, -2"
j_line = "18, 19, 22 @ -1, -1, -2"

for ii, i_line in enumerate(selected_puzzle):
    pos, velo = i_line.split("@")
    ii_pos = helper.int_str2list(pos, sep=',')[: -1]
    ii_velo = helper.int_str2list(velo, sep=',')[: -1]
    for j_line in selected_puzzle[ii:]:
        pos, velo = j_line.split("@")
        jj_pos = helper.int_str2list(pos, sep=',')[: -1]
        jj_velo = helper.int_str2list(velo, sep=',')[: -1]
        # Check for collission
        col_time = (ii_pos[0] - jj_pos[0]) / (jj_velo[0] - ii_velo[0])
        ii_pos[1] + ii_velo[1]
