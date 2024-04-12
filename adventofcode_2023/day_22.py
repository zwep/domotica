import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "22"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

selected_puzzle = puzzle_input

# Get min/max z values..?
def get_coord(x, index=-1):
    ii, jj = x.split("~")
    ii_int = helper.int_str2list(ii, sep=',')
    jj_int = helper.int_str2list(jj, sep=',')
    return ii_int[index], jj_int[index]

z = [get_coord(x) for x in selected_puzzle]
max_z_value = max(max(z))
min_z_value = min(min(z))
x = [get_coord(x, index=0) for x in selected_puzzle]
max_x_value = max(max(x))
min_x_value = min(min(x))
y = [get_coord(x, index=1) for x in selected_puzzle]
max_y_value = max(max(y))
min_y_value = min(min(y))


class Brick:
    def __init__(self, coord_str):
        self.brick_str = coord_str
        ii, jj = coord_str.split("~")
        self.ii_int = helper.int_str2list(ii, sep=',')
        self.jj_int = helper.int_str2list(jj, sep=',')
        #
        self.min_x, self.max_x = self.get_min_max(0)
        self.min_y, self.max_y = self.get_min_max(1)
        self.min_z, self.max_z = self.get_min_max(2)
        self.length_z = self.max_z - self.min_z
        self.x_range = range(self.min_x, self.max_x + 1)
        self.y_range = range(self.min_y, self.max_y + 1)
        self.z_range = range(self.min_z, self.max_z + 1)

    def get_min_max(self, index):
        return min(self.ii_int[index], self.jj_int[index]), max(self.ii_int[index], self.jj_int[index])

    def update_z_range(self):
        # But why,,?
        self.max_z = self.length_z + self.min_z
        self.z_range = range(self.min_z, self.min_z + self.length_z + 1)

    def __lt__(self, other):
        return self.min_z < other.min_z

    def __le__(self, other):
        return self.min_z <= other.min_z

    def __eq__(self, other):
        return self.min_z == other.min_z

    def __ne__(self, other):
        return self.min_z != other.min_z

    def __gt__(self, other):
        return self.min_z > other.min_z

    def __ge__(self, other):
        return self.min_z >= other.min_z

    # Nice.. dit werkt!
    def __repr__(self):
        return f"{self.min_x, self.min_y, self.min_z}~{self.max_x, self.max_y, self.max_z}"


brick_objects = [Brick(x) for x in selected_puzzle]


# empty_spaces = np.zeros((max_x_value + 1, max_y_value + 1, max_z_value + 1))
# Cant we just store all the max z-values here..?
empty_spaces = np.zeros((max_x_value + 1, max_y_value + 1))
for i_z in range(min_z_value, max_z_value + 1):
    selected_bricks = [x for x in brick_objects if i_z == x.min_z]
    for i_brick in selected_bricks:
        # Is this :, ... here required...?
        cur_z_height = empty_spaces[i_brick.x_range, i_brick.y_range]
        # If the maximum is lower than the current z-height brick...
        if np.max(cur_z_height) < i_brick.min_z:
            i_brick.min_z = int(np.max(cur_z_height) + 1)
            i_brick.update_z_range()
            empty_spaces[i_brick.x_range, i_brick.y_range] = i_brick.max_z


# Okay so this looks OK...
# How can we identify the isolated bricks..?
import itertools


def get_touching_bricks(current_brick, brick_list, level_offset='top'):
    if level_offset == 'top':
        level = current_brick.max_z + 1
    elif level_offset == 'bottom':
        level = current_brick.min_z - 1
    else:
        return None
    current_grid = set(itertools.product(current_brick.x_range, current_brick.y_range))
    top_bricks = []
    for j_brick in brick_list:
        z_bool = level in j_brick.z_range
        x_grid = set(itertools.product(j_brick.x_range, j_brick.y_range))
        # Check if there is any connection...
        xy_bool = current_grid.intersection(x_grid)
        if z_bool and xy_bool:
            # Now we have an interesting brick....
            top_bricks.append(j_brick)
    return top_bricks


possible_to_remove = []
for ii, i_brick in enumerate(brick_objects):
    top_bricks = get_touching_bricks(i_brick, brick_objects, level_offset='top')
    # If all top bricks have more than one bottom brick, then we are cool
    bottom_brick_bool = [len(get_touching_bricks(x, brick_objects, level_offset='bottom')) > 1 for x in top_bricks]
    if all(bottom_brick_bool):
        possible_to_remove.append(i_brick)

# Wow! It is done!
len(possible_to_remove)

