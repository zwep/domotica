import os
import time
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH
import matplotlib.pyplot as plt


"""
Mumbo jumbooo

What do we need....

Well, the type of rocks
Which rock is being used..
The pattern of jets
The rules for the walls/floor/etc during a jet movement
The rules for a normal downward movement

A way to store the location of the landed rocks? Or at least a count?
-> I think a set, or list of coordinates

Yeah dont store arrays, just use coordinates

"""


def change_list_order(list_format):
    # Change from [['a', 'b', 'c'], ['a', 'b', 'c']]
    # to [['a', 'a'], ['b', 'b'], ['c', 'c']]
    # and vica versa
    new_format = [[] for _ in range(len(list_format[0]))]
    for i in list_format:
        for ii, j in enumerate(i):
            new_format[ii].append(j)
            # print(f'{ii}, {j} \t {new_format}')
    return new_format


class ThisRocks:
    def __init__(self, jet_stream):
        self.jet_stream = list(jet_stream)
        self.n_jets = len(self.jet_stream)

        self.landed_coordinates = [(0, 0)]
        self.rock_encyclopedia = {0: [(0, 0), (1, 0), (2, 0), (3, 0)],
                                  1: [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
                                  2: [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
                                  3: [(0, 0), (0, 1), (0, 2), (0, 3)],
                                  4: [(0, 0), (0, 1), (1, 0), (1, 1)]}
        self.n_rocks = len(self.rock_encyclopedia)
        self.max_width = 7
        self.left_offset = 2
        self.bottom_offset = 4

        self.first_fallen_piece = []
        self.last_y_checked = 0

    def initialize_rock(self, current_coordinates):
        standard_offset = np.array([self.left_offset, self.bottom_offset])
        maximum_landed_coord = np.array([0, self.get_max_y_coord()])
        return np.array(current_coordinates) + standard_offset + maximum_landed_coord

    def get_max_y_coord(self):
        x_coord, y_coord = zip(*self.landed_coordinates)
        return max(y_coord)

    def reduce_landed_coords(self):
        # We dont need to remember everything I guess
        # Lets just do the largest 5 blocks
        self.landed_coordinates = sorted(self.landed_coordinates, key=lambda x: x[1])[-25:]

    def falling_motion(self, current_coordinates):
        # Move on down
        # Check with the walls, floor, other rocks
        # Update if necessary
        # Return updated version and if it has landed or not
        new_coordinates = current_coordinates - np.array([0, 1])
        x_coords, y_coords = map(np.array, zip(*new_coordinates))
        # landed_x_coords, landed_y_coords = map(np.array, zip(*self.landed_coordinates))
        if self.check_landed_coords(new_coordinates) or any(y_coords == 0):
            # We have landed
            return current_coordinates, False
        else:
            # We keep on falling
            return new_coordinates, True

    def check_landed_coords(self, current_coordinates):
        landed_coord_check = [tuple(x) in self.landed_coordinates for x in current_coordinates.tolist()]
        result = any(landed_coord_check)
        return result

    def jet_motion(self, jet_orientation, current_coordinates):
        # < is to the left
        # > is to the right
        if jet_orientation == '<':
            new_coordinates = current_coordinates + np.array([-1, 0])
        elif jet_orientation == '>':
            new_coordinates = current_coordinates + np.array([1, 0])
        else:
            new_coordinates = None
            print('Noooooo')

        x_coords, y_coords = map(np.array, zip(*new_coordinates))
        # Check if it is in within (0, 7) x-coord bounds.
        # And check if it is not hitting any landed block.
        if all(x_coords < self.max_width) and all(x_coords >= 0) and not self.check_landed_coords(new_coordinates):
            valid_move = True
        else:
            valid_move = False

        return new_coordinates, valid_move

    def print(self, current_coordinate):
        print(current_coordinate)

    def plot(self, current_coordinates, fig=None, ax=None, title=''):
        if fig is None:
            fig, ax = plt.subplots()

        plt.cla()
        x_coord, y_coord = zip(*self.landed_coordinates)
        ax.set_ylim(0, max(max(y_coord), 10))
        ax.set_xlim(0, self.max_width)
        obj_x_coord, obj_y_coord = zip(*current_coordinates)
        ax.scatter(x_coord, y_coord, s=10, color='k')
        ax.scatter(obj_x_coord, obj_y_coord, s=5, color='r')
        plt.pause(0.1)
        fig.suptitle(title)
        # Used to check each individual step..
        x = input()
        return fig, ax

    def reset_obj(self):
        self.landed_coordinates = [(0, 0)]

    def run_jets(self, n_landings):
        self.reset_obj()
        fig = ax = None
        jet_position_memory = [[] for _ in range(len(self.rock_encyclopedia))]
        y_coord_memory = []
        move_counter = 0
        for landed_items in range(n_landings):
            # print(landed_items, n_landings, end='\r')
            falling_rock = True
            rock_type = landed_items % self.n_rocks
            init_rock_coords = self.rock_encyclopedia[rock_type]
            current_coordinates = self.initialize_rock(init_rock_coords)
            while falling_rock:
                jet_move = self.jet_stream[move_counter % self.n_jets]
                move_counter += 1
                new_coords, valid_motion = self.jet_motion(jet_orientation=jet_move, current_coordinates=current_coordinates)
                if valid_motion is True:
                    current_coordinates = new_coords
                new_coords, falling_rock = self.falling_motion(current_coordinates)
                if falling_rock is True:
                    current_coordinates = new_coords
                else:
                    jet_position_memory[rock_type].append(move_counter % self.n_jets)
                    last_y_max = max(self.landed_coordinates, key=lambda x: x[1])[1]
                    y_coord_memory.append(last_y_max)
            self.landed_coordinates.extend([tuple(x) for x in current_coordinates])
        return jet_position_memory, y_coord_memory


puzzle_input_test = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
dfile = os.path.join(DPATH, 'day17.txt')
with open(dfile, 'r') as f:
    puzzle_input = f.read().strip()


this_rock = ThisRocks(puzzle_input)
n_iter_part2 = 5000
result, y_result = this_rock.run_jets(n_iter_part2)
result_2 = change_list_order(result)

xcoord, ycoord = zip(*this_rock.landed_coordinates)
print('Max y coord ', max(ycoord))

fig, ax = plt.subplots()
for ii in result:
    ax.plot(ii)
ax.plot(result_2[1])

real_case_pattern = '20		29		33		42		46'
for ii, i_res in enumerate(result_2[:-1]):
    str_pattern = '\t\t'.join([str(x) for x in i_res])
    object_height_result = f'\t {(ii + 1) * 5} {y_result[(ii + 1) * 5]}'
    if str_pattern == real_case_pattern:
        print(str_pattern, object_height_result)

for ii, i_res in enumerate(result_2[685:695]):
    str_pattern = '\t\t'.join([str(x) for x in i_res])
    object_height_result = f'\t {(ii + 1) * 5} {y_result[(ii + 1) * 5]}'
    print(str_pattern)


# For the test case...
target_n_object = 1e12
base_line_n_obj = 20
base_line_height = 36
increment_height = 53
increment_obj = 35

remaining_object = int(target_n_object - base_line_n_obj)
factor_height = int(remaining_object / increment_obj)
residual_object = remaining_object - factor_height * increment_obj

print('Remaining', residual_object)

print('Result ', factor_height * increment_height + base_line_height)

# For the real case...
target_n_object = 1e12
base_line_n_obj = 1730
base_line_height = 2729
increment_height = 2709
increment_obj = 1725

remaining_object = int(target_n_object - base_line_n_obj)
factor_height = int(remaining_object / increment_obj)
residual_object = remaining_object - factor_height * increment_obj
residual_height = y_result[base_line_n_obj+residual_object] - base_line_height
print('Remaining', residual_object)

factor_height * increment_height + base_line_height + residual_height
