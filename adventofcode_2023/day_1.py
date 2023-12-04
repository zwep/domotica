import numpy as np
import os
import matplotlib.pyplot as plt
import re
from advent_of_code_helper.helper import read_lines, fetch_data, read_lines_strip, fetch_test_data
from advent_of_code_helper.configuration import DDATA_YEAR


def get_line_number(i_line):
    first_digit = re.search('([0-9])', i_line).groups()[0]
    second_digit = re.search('([0-9])', i_line[::-1]).groups()[0]
    line_number = int(first_digit + second_digit)
    return line_number


def get_str(search_obj_list, convert_dict):
    search_obj = search_obj_list[0]
    value = search_obj.group()
    if value in convert_dict.keys():
        str_value = str(convert_dict[value])
    else:
        str_value = value
    return str_value

DAY = "1"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = fetch_data(DAY)
_ = fetch_test_data(DAY)

test_puzzle_input = read_lines_strip(DDATA_DAY_TEST)

# First
if False:
    puzzle_input = read_lines(DDATA_DAY)
    s = 0
    for i_line in puzzle_input:
        line_number = get_line_number(i_line)
        s += line_number

# Second
convert_dict = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
digit_list = list(convert_dict.keys()) + [str(x) for x in list(convert_dict.values())]

puzzle_input = read_lines_strip(DDATA_DAY)
s = 0
for i_line in puzzle_input:
    search_obj_list = []
    for k in digit_list:
        temp_search_obj = list(re.finditer(k, i_line))
        if temp_search_obj is not None:
            search_obj_list.extend(temp_search_obj)

    sorted_search_obj_list = sorted(search_obj_list, key=lambda x: x.span()[0])
    rev_sorted_search_obj_list = sorted(search_obj_list, key=lambda x: x.span()[0], reverse=True)

    first_str_value = get_str(sorted_search_obj_list, convert_dict)
    last_str_value = get_str(rev_sorted_search_obj_list, convert_dict)

    line_number = int(first_str_value + last_str_value)
    s += line_number

s

# 54270
# 54704 too low
# 54709 too high

# 54761 wrong