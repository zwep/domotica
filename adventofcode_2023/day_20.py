import numpy as np
import os
import re
import matplotlib.pyplot as plt
from advent_of_code_helper.helper import read_lines_strip, fetch_data, fetch_test_data
from advent_of_code_helper.configuration import DDATA_YEAR


def day1(x_input):
    return None


def day2(x_input):
    return None


DAY = "20"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = fetch_data(DAY)
_ = fetch_test_data(DAY)

# read input
puzzle_input = read_lines_strip(DDATA_DAY)
test_puzzle_input = read_lines_strip(DDATA_DAY_TEST)