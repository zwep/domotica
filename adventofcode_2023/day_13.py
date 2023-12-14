import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def parse_input(input_list):
    collection = []
    temp = []
    for i_line in input_list:
        if i_line == '':
            collection.append(temp)
            temp = []
        else:
            temp.append(i_line)
    else:
        collection.append(temp)
    return collection


def convert2int(i_line):
    # Convert the dots to an int and the # too
    i_line = re.sub('#', '1', i_line)
    i_line = re.sub('\.', '2', i_line)
    return int(i_line)


def convert2str(i_line):
    # Convert the dots to an int and the # too
    i_line = re.sub('#', '1', i_line)
    i_line = re.sub('\.', '2', i_line)
    return i_line


DAY = "13"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)


def string2mirror_count(x):
    # Convert to large ints
    int_list = [convert2int(x) for x in x]
    n_items = len(int_list)
    # Get the difference
    difference_list = helper.difference_element_list(int_list)
    zero_index_list = [i for i, x in enumerate(difference_list) if x == 0]
    #
    calculation_stuff = {}
    for i_index in zero_index_list:
        i_delta = 0
        # Continue while we are INSIDE the array
        while ((i_index + i_delta + 1) < n_items) and ((i_index - i_delta) >= 0):
            if int_list[i_index - i_delta] != int_list[i_index + i_delta + 1]:
                break
            i_delta += 1
        # Once we have successfully exited the array, we count it as a mirror
        else:
            calculation_stuff.setdefault(i_index, 1)
    return calculation_stuff


def string2mirror_count_part2(x, memory_index):
    # Convert to large ints
    int_list = [convert2int(x) for x in x]
    n_items = len(int_list)
    str_int_list = [[int(x) for x in convert2str(x)] for x in x]
    # Get a new difference, WITH slack
    zero_index_list = []
    for ii in range(n_items-1):
        sum_diff = sum([abs(x - y) for x, y in zip(str_int_list[ii], str_int_list[ii + 1])])
        if sum_diff == 0:
            # Here we incorporate that we want a different mirror
            if ii != memory_index:
                zero_index_list.append((ii, True))
        elif sum_diff == 1:
            # Here we incorporate that we want a different mirror
            if ii != memory_index:
                zero_index_list.append((ii, True))
        else:
            pass
    #
    calculation_stuff = {}
    for i_index, slack_variable in zero_index_list:
        i_delta = 0
        # Continue while we are INSIDE the array
        while ((i_index + i_delta + 1) < n_items) and ((i_index - i_delta) >= 0):
            if int_list[i_index - i_delta] != int_list[i_index + i_delta + 1]:
                sum_diff = sum([abs(x - y) for x, y in zip(str_int_list[i_index - i_delta], str_int_list[i_index + i_delta + 1])])
                if (sum_diff == 1) and slack_variable:
                    slack_variable = False
                else:
                    break
            i_delta += 1
        # Once we have successfully exited the array, we count it as a mirror
        else:
            calculation_stuff.setdefault(i_index, 1)
    return calculation_stuff


def get_max_key_value(x_dict):
    if x_dict:
        max_key = max(x_dict, key=lambda x: x_dict[x])
        max_value = x_dict[max_key]
    else:
        max_key = max_value = -1
    return max_key, max_value


ash_and_rock_list = parse_input(puzzle_input)
total_sum = 0
ash_memory = []
for jj, i_ash_rock in enumerate(ash_and_rock_list):
    temp = [-1, -1]
    mirror_count_rows = string2mirror_count(i_ash_rock)
    if mirror_count_rows:
        max_key_row, max_value_row = get_max_key_value(mirror_count_rows)
        total_sum += 100 * (max_key_row + 1)
        temp[0] = max_key_row  # Store this information for later...
    else:
        i_ash_rock_col = helper.transpose_of_nested_list(i_ash_rock, to_str=True)
        mirror_count_cols = string2mirror_count(i_ash_rock_col)
        max_key_col, max_value_col = get_max_key_value(mirror_count_cols)
        total_sum += (max_key_col + 1)
        temp[1] = max_key_col  # Store this information for later...
    ash_memory.append(temp)

print(total_sum)
# So now we know which input has what kind of output...
# How to use this..

"""
Part 2
"""

total_sum = 0
# So now we pass one what we did...
for jj, i_ash_rock in enumerate(ash_and_rock_list):
    mirror_count_rows = string2mirror_count_part2(i_ash_rock, memory_index=ash_memory[jj][0])
    # print(mirror_count_rows)
    if mirror_count_rows:
        max_key_row, max_value_row = get_max_key_value(mirror_count_rows)
        total_sum += 100 * (max_key_row + 1)
    else:
        i_ash_rock_col = helper.transpose_of_nested_list(i_ash_rock, to_str=True)
        mirror_count_cols = string2mirror_count_part2(i_ash_rock_col, memory_index=ash_memory[jj][1])
        max_key_col, max_value_col = get_max_key_value(mirror_count_cols)
        total_sum += (max_key_col + 1)


print(total_sum)