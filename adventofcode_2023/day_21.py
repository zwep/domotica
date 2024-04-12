import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def get_valid_steps(irow, icol, puzzle_map, visited_position):
    max_row = len(puzzle_map)
    max_col = len(puzzle_map[0])
    possible_position = []
    for _, delta_pos in helper.DIR2POS.items():
        delta_row, delta_col = delta_pos
        new_row = delta_row + irow
        new_col = delta_col + icol
        if not ((new_row, new_col) in visited_position) and \
                (0 <= new_row < max_row) and \
                (0 <= new_col < max_col):
            next_position = puzzle_map[new_row][new_col]
            if next_position == '.' or next_position == 'S':
                possible_position.append((new_row, new_col))
    return possible_position


DAY = "21"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

selected_puzzle = puzzle_input

remaining_steps = 64
starting_position = [(ii, i_line.index('S')) for ii, i_line in enumerate(selected_puzzle) if 'S' in i_line]

max_col = len(selected_puzzle)
steps_to_visit = starting_position
what_can_we_reach = []
for i in range(remaining_steps):
    next_step_list = []
    for i_steps_to_visit in steps_to_visit:
        next_steps = get_valid_steps(*i_steps_to_visit, selected_puzzle, [])
        for i_next_step in next_steps:
            if i_next_step not in next_step_list:
                next_step_list.append(i_next_step)
    else:
        what_can_we_reach.append(next_step_list)
        steps_to_visit = next_step_list


step_array = np.zeros((max_col, max_col))

fig, ax = plt.subplots()
imshow_ax = ax.imshow(step_array, vmin=[0, 1])
for i, ix in enumerate(what_can_we_reach):
    step_array = np.zeros((max_col, max_col))
    for i_coord in ix:
        step_array[i_coord] = 1
    imshow_ax.set_data(step_array)
    ax.set_title(i)
    plt.pause(0.2)

# Answer part 1
len(set(what_can_we_reach[-1]))