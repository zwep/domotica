import numpy as np
import math
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def get_empty_rows_cols(puzzle_input):
    MAX_lines = len(puzzle_input)
    MAX_char = len(puzzle_input[0])

    # Find rows and columns with only dots
    empty_rows = [ii for ii, i_line in enumerate(puzzle_input) if len(set(i_line)) == 1]
    empty_cols = []
    for i_char in range(MAX_char):
        temp_col = []
        for i_line in range(MAX_lines):
            temp_col.append(puzzle_input[i_line][i_char])
        if len(set(temp_col)) == 1:
            empty_cols.append(i_char)
    return empty_rows, empty_cols


def manhattan_distance(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def get_galaxy_coords(puzzle_input):
    MAX_lines = len(puzzle_input)
    MAX_char = len(puzzle_input[0])
    galaxy_coords = []
    for ii in range(MAX_lines):
        for jj in range(MAX_char):
            if puzzle_input[ii][jj] == '#':
                galaxy_coords.append((ii, jj))
    return galaxy_coords


DAY = "11"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

selected_puzzle = test_puzzle_input
# selected_puzzle = puzzle_input
empty_rows, empty_cols = get_empty_rows_cols(selected_puzzle)

MAX_char = len(selected_puzzle[0])

# Add lines from furthers to lowest, so that distance from 0 remains the same
for ii in sorted(empty_rows)[::-1]:
    temp_row = ''. join(['.'] * MAX_char)
    selected_puzzle.insert(ii, temp_row)

MAX_lines = len(selected_puzzle)

# Now add columns...
for i_char in sorted(empty_cols)[::-1]:
    for i_line in range(MAX_lines):
        temp_list = list(selected_puzzle[i_line])
        temp_list.insert(i_char, '.')
        selected_puzzle[i_line] = ''.join(temp_list)

MAX_char = len(selected_puzzle[0])

"""
Done..?
"""
galaxy_coords = get_galaxy_coords(selected_puzzle)

n_galaxies = len(galaxy_coords)
hoppa = np.zeros((n_galaxies, n_galaxies))
for i_galax in range(n_galaxies):
    for j_galax in range(i_galax, n_galaxies):
        hoppa[i_galax, j_galax] = manhattan_distance(galaxy_coords[i_galax], galaxy_coords[j_galax])

hoppa.sum()

"""
Okay cool
Start over
"""

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

# selected_puzzle = test_puzzle_input
selected_puzzle = puzzle_input
empty_rows, empty_cols = get_empty_rows_cols(selected_puzzle)

space_time_step = 1e6 - 1
galaxy_coords = get_galaxy_coords(selected_puzzle)

n_galaxies = len(galaxy_coords)
hoppa = np.zeros((n_galaxies, n_galaxies))
i_galax = 0
j_galax = 2
for i_galax in range(n_galaxies):
    for j_galax in range(i_galax, n_galaxies):
        src = galaxy_coords[i_galax]
        dest = galaxy_coords[j_galax]
        hoppa[i_galax, j_galax] = manhattan_distance(src, dest)
        for space_time_hole in empty_rows:
            if space_time_hole in range(min(dest[0], src[0])+1, max(src[0], dest[0])+1):
                hoppa[i_galax, j_galax] += space_time_step
        for space_time_hole in empty_cols:
            if space_time_hole in range(min(dest[1], src[1])+1, max(src[1], dest[1])+1):
                hoppa[i_galax, j_galax] += space_time_step

# 10276166
hoppa.sum()

galaxy_coords