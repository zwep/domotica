import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def roll_north(platform):
    n_cols = len(platform[0])
    rolled_input = ['#'.join([''.join(sorted(x)[::-1]) for x in helper.get_column(platform, i_col, to_str=True).split('#')]) for i_col in range(n_cols)]
    rolled_north = helper.transpose_of_nested_list(rolled_input, to_str=True)
    return rolled_north


def roll_east(platform):
    n_rows = len(platform)
    rolled_east = ['#'.join([''.join(sorted(x)[::-1]) for x in platform[i_row][::-1].split('#')])[::-1] for i_row in range(n_rows)]
    return rolled_east


def roll_south(platform):
    # Do ::-1 after get column
    # And again when the operation is completed
    n_cols = len(platform[0])
    rolled_input = ['#'.join([''.join(sorted(x)[::-1]) for x in helper.get_column(platform, i_col, to_str=True)[::-1].split('#')])[::-1] for i_col in range(n_cols)]
    rolled_south = helper.transpose_of_nested_list(rolled_input, to_str=True)
    return rolled_south


def roll_west(platform):
    n_rows = len(platform)
    rolled_east = ['#'.join([''.join(sorted(x)[::-1]) for x in platform[i_row].split('#')]) for i_row in range(n_rows)]
    return rolled_east


def get_load(platform):
    n_cols = len(platform[0])
    return sum([(n_cols - ii) * x.count('O') for ii, x in enumerate(platform)])


def perform_cycle(x):
    x = roll_north(x)
    x = roll_west(x)
    x = roll_south(x)
    x = roll_east(x)
    return x

DAY = "14"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

"""
Rock and roll...
"""

selected_puzzle = puzzle_input
# Is this it..?
n_cols = len(selected_puzzle[0])
rolled_north = roll_north(selected_puzzle)
result = get_load(rolled_north)

print(result)

"""
Part 2
"""

selected_puzzle = test_puzzle_input
# Is this it..?
x = np.copy(selected_puzzle).tolist()
result = get_load(x)
n_cycle = 400
load_weight = []
for i in range(3):
    x = perform_cycle(x)
    result = get_load(x)
    print(i, result)
    load_weight.append(result)

# we know that from 200 onwards the period repeats...
n_test_cycle = 100
max_weight = max(load_weight[n_test_cycle:])
diff_weight = np.diff(np.where(np.array(load_weight) == max_weight)[0])
period_size = np.abs(np.diff(diff_weight))[-1] + diff_weight[-1]  # .. this?

# period_size = list(set(list(np.diff(np.where(np.array(load_weight) == max_weight)))[0]))[0]
first_index = load_weight[n_test_cycle:].index(max_weight)
# Fun visualization
fig, ax = plt.subplots()
ax.plot(load_weight)
ax.plot(range(first_index + n_test_cycle, n_cycle), load_weight[(first_index + n_test_cycle):])
ax.plot(range(first_index + n_test_cycle + period_size, n_cycle), load_weight[(first_index + n_test_cycle + period_size):])

# Okay...
target_cycle = 1000000000
remainder = (target_cycle - (first_index + n_test_cycle)) % (period_size )
load_weight[first_index + n_test_cycle: first_index + n_test_cycle + remainder][-1]

set(load_weight[first_index + n_test_cycle:(first_index + n_test_cycle + period_size)])
# 86096 too high
# 86086 too high
# 86066 too low
# 86083 nope
# 86069
