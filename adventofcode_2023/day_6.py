import numpy as np
import os
import re
import matplotlib.pyplot as plt
from advent_of_code_helper.helper import read_lines_strip, fetch_data, fetch_test_data
from advent_of_code_helper.configuration import DDATA_YEAR

from advent_of_code_helper.helper import int_str2list


def day1(x_input):
    return None


def day2(x_input):
    return None


DAY = "6"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = fetch_data(DAY)
_ = fetch_test_data(DAY)

# read input
puzzle_input = read_lines_strip(DDATA_DAY)
test_puzzle_input = read_lines_strip(DDATA_DAY_TEST)

selected_input = puzzle_input
time_list = int_str2list(selected_input[0].split(':')[1])
game_list = int_str2list(selected_input[1].split(':')[1])
n_races = len(time_list)
# Allowed time, max distance
possibilities = []
for i_race in range(n_races):
    print('\t', time_list[i_race], game_list[i_race])
    T = time_list[i_race]
    D = game_list[i_race]
    V1 = (-T + (T ** 2 - 4 * (D+1)) ** 0.5) / (-2)
    V2 = (-T - (T ** 2 - 4 * (D+1)) ** 0.5) / (-2)
    T1 = np.ceil(min(V1, V2))
    T2 = np.floor(max(V1, V2))
    print(T2 - T1 + 1)
    diff = T2 - T1 + 1
    possibilities.append(diff)

np.prod(possibilities)

T = int(''.join(selected_input[0].split(':')[1].split(' ')))
D = int(''.join(selected_input[1].split(':')[1].split(' ')))

V1 = (-T + (T ** 2 - 4 * (D+1)) ** 0.5) / (-2)
V2 = (-T - (T ** 2 - 4 * (D+1)) ** 0.5) / (-2)
T1 = np.ceil(min(V1, V2))
T2 = np.floor(max(V1, V2))
# print(T2 - T1 + 1)
diff = T2 - T1 + 1
print(diff)