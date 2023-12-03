import numpy as np
import re
import os
import matplotlib.pyplot as plt
from advent_of_code_helper.helper import read_lines_strip, fetch_data
from advent_of_code_helper.configuration import DDATA_YEAR


def get_digit(integer_coord, input_data):
    integer_str = ''
    for i, j in integer_coord:
        integer_str += input_data[i][j]
    return int(integer_str)


def neighbours(i, j, input_data):
    n_lines = len(input_data)
    n_char = len(input_data[0])
    for i_delta in [-1, 0, 1]:
        for j_delta in [-1, 0, 1]:
            line_coord = min(max(i + i_delta, 0), n_lines-1)
            char_coord = min(max(j + j_delta, 0), n_char-1)
            yield input_data[line_coord][char_coord]


def neighbours_digit(i, j, input_data):
    n_lines = len(input_data)
    n_char = len(input_data[0])
    for i_delta in [-1, 0, 1]:
        for j_delta in [-1, 0, 1]:
            line_coord = min(max(i + i_delta, 0), n_lines-1)
            char_coord = min(max(j + j_delta, 0), n_char-1)
            neighbour_value = input_data[line_coord][char_coord]
            if neighbour_value.isdigit():
                yield (line_coord, char_coord)


def get_special_char(x_str):
    return [x for x in set(x_str) if not x.isdigit() and x != '.']


def get_coord(i_line, i_coord, step):
    current_char = i_line[i_coord]
    end_of_line = False
    while (current_char not in special_characters + ['.']) and not end_of_line:
        i_coord += step
        if i_coord < 0 or i_coord >= len(i_line):
            end_of_line = True
        else:
            current_char = i_line[i_coord]
    return i_coord


def get_int_value(i_line_coord, j_char_coord):
    left_coord = get_coord(input_data[i_line_coord], j_char_coord, step=-1)
    right_coord = get_coord(input_data[i_line_coord], j_char_coord, step=1)
    int_value = input_data[i_line_coord][(left_coord+1):right_coord]
    return int(int_value)


def get_all_unique_int_values(neighbour_digit_list):
    for i_line_coord, j_char_coord in neighbour_digit_list:
        yield get_int_value(i_line_coord, j_char_coord)


DAY = "3"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')

# Run get data..
_ = fetch_data(DAY)

input_data = ["467..114..",
"...*......",
"..35..633.",
"......#...",
"617*......",
".....+.58.",
"..592.....",
"......755.",
"...$.*....",
".664.598.."]

# read input
input_data = read_lines_strip(DDATA_DAY)
input_data_str = ''.join(input_data)
special_characters = list(get_special_char(input_data_str))


integer_collection = []
integer_list = []
for i, i_line in enumerate(input_data):
    for j, i_char in enumerate(i_line):
        if i_char in ['.'] + special_characters:
            if len(integer_list):
                integer_collection.append(integer_list)
            integer_list = []
        elif i_char.isdigit():
            integer_list.append([i, j])

# Now check if there are special characters around the integers
valid_machine_integer = []
for i_integer in integer_collection:
    neighbour_string = ''
    for i_coord, j_coord in i_integer:
        neighbour_string += ''.join(list(neighbours(i_coord, j_coord, input_data)))
    sample_special_char = set(get_special_char(neighbour_string))
    if len(sample_special_char):
        valid_int = get_digit(i_integer, input_data)
        valid_machine_integer.append(valid_int)

#           525119
sum(valid_machine_integer)

"""
Part 2

Now we do the reverse... not find the ints, but find the *.
Get the neighbours. Then find the ints again...?
"""

gear_collection = []
for i, i_line in enumerate(input_data):
    for j, i_char in enumerate(i_line):
        if i_char == '*':
            gear_collection.append([i, j])

valid_gear_list = []
for i_gear, j_gear in gear_collection:
    neighbour_digit_list = list(neighbours_digit(i_gear, j_gear, input_data))
    unique_values = set(get_all_unique_int_values(neighbour_digit_list))
    if len(unique_values) == 2:
        print(unique_values)
        prod_value = 1
        for ii in unique_values:
            prod_value *= ii
        valid_gear_list.append(prod_value)

# 76019682
sum(valid_gear_list)
