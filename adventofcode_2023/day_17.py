import numpy as np
import math
import itertools
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def str2list(x):
    return list(map(int, x.split(',')))


def list2str(x):
    return ','.join([str(ix) for ix in x])


def update_position(cur_pos, delta_pos):
    return [cur_pos[0] + delta_pos[0], cur_pos[1] + delta_pos[1]]




DAY = "17"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

selected_puzzle = [list(x) for x in puzzle_input]
selected_puzzle = np.array(selected_puzzle).astype(int)

"""
Lets practice Dijkstra
"""

max_line = len(selected_puzzle)
max_col = len(selected_puzzle[0])
min_rage = 4
max_range = 10  # Of the steps we can take in one direction....
direction2pos = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1]}
east_west_list = ['E' * ii for ii in range(min_rage, max_range + 1)] + ['W' * ii for ii in range(min_rage, max_range + 1)]
north_south_list = ['N' * ii for ii in range(min_rage, max_range + 1)] + ['S' * ii for ii in range(min_rage, max_range + 1)]

vertex = itertools.product(range(max_line), range(max_col), range(2))
distance_to_end = {}
# Initialize
distance_to_end.setdefault(list2str([0, 0, 0]), 0)
distance_to_end.setdefault(list2str([0, 0, 1]), 0)
for i_vertex in vertex:
    distance_to_end.setdefault(list2str(i_vertex), math.inf)

max_iterations = len(distance_to_end) - 1
# max_iterations = 2
for i_iter in range(max_iterations):
    print(i_iter, max_iterations, end='\r')
    # Lets update all the edges...
    prev_value_list = np.array(list(distance_to_end.values()))
    for i_vertex, i_vertex_dist in distance_to_end.items():
        if np.isinf(i_vertex_dist):
            continue
        # print(i_vertex)
        # break
        # Get the neighbours...
        # print(i_vertex)
        neighbour_direction_list = []
        current_row, current_col, direction_id = str2list(i_vertex)
        current_pos = [current_row, current_col]
        # This means that we have moved over rows. Now we only allow for East or West
        if direction_id > 0:
            neighbour_direction_list.extend(east_west_list)
        # If it is zero, then this means that we have moved over columns. Now we only allow for North or East
        else:
            neighbour_direction_list.extend(north_south_list)

        # Convert the neighbours to vertex keys
        neighbour_vertex_list = []
        for x in neighbour_direction_list:
            # Get the unique character
            unique_dir = ''.join(set(x))
            # Get the displacement vector
            delta_pos = [len(x) * i_delta for i_delta in direction2pos[unique_dir]]
            # And the history of how far we reached
            temp_direction_id = 1 if unique_dir in ['N', 'S'] else 0
            # Combine this into the vertex key
            neighbour_position = update_position(current_pos, delta_pos)
            neighbour_vertex = list2str(neighbour_position + [temp_direction_id])
            if neighbour_vertex in distance_to_end:
                neighbour_vertex_list.append(neighbour_vertex)
                # j_vertex = neighbour_vertex
                # new_row, new_col = neighbour_position
                # distance_to_end[j_vertex] = min(distance_to_end[j_vertex],
                #                                 int(selected_puzzle[new_row][new_col]) + distance_to_end[i_vertex])
        # print(neighbour_vertex_list)
        # Now we have the vertex neighbours.... and we can update the dist function..!
        for j_vertex in neighbour_vertex_list:
            new_row, new_col, _ = str2list(j_vertex)
            row_start = min(current_row + 1, new_row)
            row_end = max(current_row - 1, new_row) + 1
            #
            col_start = min(current_col + 1, new_col)
            col_end = max(current_col - 1, new_col) + 1
            value_list = selected_puzzle[row_start:row_end, col_start:col_end].reshape(-1).tolist()
            # print(value_list)
            summed_value = sum(value_list)
            distance_to_end[j_vertex] = min(distance_to_end[j_vertex], summed_value + distance_to_end[i_vertex])

    if all(prev_value_list == np.array(list(distance_to_end.values()))):
        break
        # for j_vertex in neighbour_vertex_list:
        #     print(distance_to_end[j_vertex])
        # print()

print(distance_to_end)

min(distance_to_end['12,12,0'], distance_to_end['12,12,1'])


for k, v in distance_to_end.items():
    print(k, v)