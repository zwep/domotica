import numpy as np
import itertools
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def array2str(input_array):
    return ''.join(input_array.tolist())


def get_count_str(i_line):
    return ','.join([str(x.count('#')) for x in i_line.split('.') if '#' in x])


def get_input_target(i_line):
    return i_line.split(" ")


DAY = "12"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

# Ik weet nog niet hoe ik de passende informatie ga gebruiken...
# Ik weet dat ik het aantal groepen kan gebruiken, en da grootte per groep..
# Maar hoe ik dat precies fit aan wat ik vind... vind ik lastig


def get_succes_counts(puzzle_line):
    input_line, target_line = get_input_target(puzzle_line)
    n_question_mark = input_line.count('?')
    stack_iterator = itertools.product('.#', repeat=n_question_mark)
    succes_counter = 0
    for i_stack in stack_iterator:
        # Oke dus dit kan..
        z = np.array(list(input_line))
        z[z == '?'] = list(i_stack)
        result = get_count_str(array2str(z))
        if result == target_line:
            succes_counter += 1

    return succes_counter

# lol.. This runs for a couple of minutes, which is fine for part 1
the_chosen_one = [get_succes_counts(x) for x in puzzle_input]
sum(the_chosen_one)

"""
Modifying input
"""

input_line, target_line = get_input_target(test_puzzle_input[0])
new_input_line = '?'.join([input_line] * 5)
new_target_line = ','.join([target_line] * 5)
# Okay and now we go....
