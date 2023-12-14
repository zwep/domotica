import numpy as np
import os
import re
import matplotlib.pyplot as plt
from advent_of_code_helper.helper import read_lines_strip, fetch_data, fetch_test_data
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def get_neighbours(ii, jj, coordinates_visited, neighbours_found=None):
    """
    Gets all the neighvours of ii, jj bounded by the coordinates_visited content (
    :param ii:
    :param jj:
    :param coordinates_visited:
    :return:
    """
    stack_to_visit = [(ii, jj)]
    # Make it so that we can initialze with a set of neighbours
    if neighbours_found is None:
        neighbours_found = []
    while len(stack_to_visit):
        ii, jj = stack_to_visit.pop()
        if (ii, jj) in coordinates_visited:
            continue
        elif (ii, jj) in neighbours_found:
            continue
        elif (ii < 0) or (ii > MAX_lines):
            continue
        elif (jj < 0) or (jj > MAX_char):
            continue
        else:
            neighbours_found.append((ii, jj))
            for k, v in direction2pos.items():
                delta_ii, delta_jj = v
                # Update position
                stack_to_visit.append((ii + delta_ii, jj + delta_jj))

    return neighbours_found


def update_loc(ii, jj, LR_dir):
    """
    Helper function to upadte a positino
    :param ii:
    :param jj:
    :param LR_dir:
    :return:
    """
    delta_ii, delta_jj = direction2pos[LR_dir]
    return ii + delta_ii, jj + delta_jj


DAY = "10"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = fetch_data(DAY)
_ = fetch_test_data(DAY)

# read input
puzzle_input = read_lines_strip(DDATA_DAY)
test_puzzle_input = read_lines_strip(DDATA_DAY_TEST)

pipe2neighbours = {'|': ['N', 'S'], '-': ['E', 'W'], 'L': ['N', 'E'], '.': [],
                   'J': ['N', 'W'], '7': ['W', 'S'], 'F': ['S', 'E'], 'S': ['N', 'E', 'S', 'W']}

direction2pos = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1]}
direction2LR = {'N': ['W', 'E'], 'E': ['N', 'S'], 'S': ['E', 'W'], 'W': ['S', 'N']}
pos2inverse = {'S': 'N', 'E': 'W', 'W': 'E', 'N': 'S', None: 'None'}


selected_puzzle = puzzle_input

MAX_lines = len(selected_puzzle)
MAX_char = len(selected_puzzle[0])

start_i, start_j = zip(*[(ii, x.index('S')) for ii, x in enumerate(selected_puzzle) if 'S' in x])

ii = start_i[0]
jj = start_j[0]
count = 0
current_char = selected_puzzle[ii][jj]
prev_direction = None
coordinates_visited = []
local_left_coordinates = []
local_right_coordinates = []
while not (current_char == 'S' and count > 0):
    # For part 2
    coordinates_visited.append((ii, jj))
    if prev_direction is not None:
        left_dir, right_dir = direction2LR[prev_direction]
        local_left_coordinates.append(update_loc(ii, jj, left_dir))
        local_right_coordinates.append(update_loc(ii, jj, right_dir))
        #
        temp_delta_i, temp_delta_j = direction2pos[pos2inverse[prev_direction]]
        local_left_coordinates.append(update_loc(ii + temp_delta_i, jj + temp_delta_j, left_dir))
        local_right_coordinates.append(update_loc(ii + temp_delta_i, jj + temp_delta_j, right_dir))

    direction_list = pipe2neighbours[current_char]
    # Dont go back...
    direction_list = [x for x in direction_list if x != pos2inverse[prev_direction]]
    new_direction_list = []
    for sel_dir in direction_list:
        delta_ii, delta_jj = direction2pos[sel_dir]
        if ((ii + delta_ii) < 0) or ((ii + delta_ii) > MAX_lines):
            continue
        if ((jj + delta_jj) < 0) or ((jj + delta_jj) > MAX_char):
            continue
        # Check next char if we can even go there by inverting the neighbours of the next char
        next_char = selected_puzzle[ii + delta_ii][jj + delta_jj]
        if sel_dir not in ''.join([pos2inverse[x] for x in pipe2neighbours[next_char]]):
            continue

        new_direction_list.append(sel_dir)

    # print('Status')
    # print('\t Cur char ', current_char, f'({ii}, {jj})')
    if count == 0:
        prev_direction = new_direction_list[1]
    else:
        prev_direction = new_direction_list[0]
    # print('\t New direction ', prev_direction)
    delta_ii, delta_jj = direction2pos[prev_direction]
    # Update position
    ii = ii + delta_ii
    jj = jj + delta_jj
    # Update character
    current_char = selected_puzzle[ii][jj]
    # print('\t New char ', current_char, f'({ii}, {jj})')
    count += 1
    # Print status

print(' Solution 1', count / 2)

"""
"""

len(local_left_coordinates)
len(local_right_coordinates)
# Now we have all the left coordinates
all_left_neighbours = []
for sel_coord in local_left_coordinates:
    all_left_neighbours = get_neighbours(*sel_coord, coordinates_visited, all_left_neighbours)

print('Left ', len(all_left_neighbours))
# Now we have all the left coordinates
all_right_neighbours = []
for sel_coord in local_right_coordinates:
    all_right_neighbours = get_neighbours(*sel_coord, coordinates_visited, all_right_neighbours)

print('Right ', len(all_right_neighbours))


"""
Debug test case
"""


if MAX_lines < 100:
    for ii in range(MAX_lines):
        temp_left_str = ''
        temp_path_str = ''
        temp_right_str = ''
        for jj in range(MAX_char):
            cur_char = selected_puzzle[ii][jj]
            if (ii, jj) in local_left_coordinates: #all_left_neighbours:
                temp_left_str += helper.Color.RED + cur_char + helper.Color.END
            else:
                temp_left_str += cur_char

            if (ii, jj) in local_right_coordinates: #all_right_neighbours:
                temp_right_str += helper.Color.BLUE + cur_char + helper.Color.END
            else:
                if (ii, jj) in missing_coords:  # all_right_neighbours:
                    temp_right_str += helper.Color.PURPLE + cur_char + helper.Color.END
                else:
                    temp_right_str += cur_char

            if (ii, jj) in coordinates_visited:
                temp_path_str += helper.Color.GREEN + cur_char + helper.Color.END
            else:
                if (ii, jj) in missing_coords:  # all_right_neighbours:
                    temp_path_str += helper.Color.PURPLE + cur_char + helper.Color.END
                else:
                    temp_path_str += cur_char

        # temp_print = temp_left_str + '\t' + temp_path_str + '\t' + temp_right_str
        # temp_print = temp_right_str
        temp_print = temp_path_str
        print(ii, re.sub('\.', ',', temp_print))

