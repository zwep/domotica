import os
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH
import matplotlib.pyplot as plt
import string
import itertools


def process_coord(coord_str, correction_x):
    # Here we correct for the large x values
    new_coord = list(map(int, coord_str.split(",")))
    new_coord[0] -= correction_x
    return new_coord


def get_blank_cave(puzzle_input):
    # First get all the x coords and y coords
    x_coords, y_coords = zip(*list(itertools.chain(*[[map(int, x.split(',')) for x in y.split('->')] for y in puzzle_input])))
    height = max(y_coords) + 6
    min_xcoord = min(x_coords) - height
    max_xcoord = max(x_coords) + height

    width = max_xcoord - min_xcoord + 2
    puzzle_cave = np.zeros((width, height), dtype=str)
    puzzle_cave[puzzle_cave == ''] = '.'

    return puzzle_cave, min_xcoord, max(y_coords)


def fill_cave_with_rocks(puzzle_input, puzzle_cave, correction_coord):
    for i_puzzle in puzzle_input:
        coord_list = i_puzzle.split(' -> ')
        for i_coord in range(len(coord_list)-1):
            start_coord = process_coord(coord_list[i_coord], correction_coord)
            end_coord = process_coord(coord_list[i_coord+1], correction_coord)
            puzzle_cave[start_coord[0]: end_coord[0]+1, start_coord[1]:end_coord[1]+1] = '#'
            puzzle_cave[end_coord[0]: start_coord[0]+1, end_coord[1]:start_coord[1]+1] = '#'

    puzzle_cave[500 - correction_coord, 0] = '+'
    return puzzle_cave


class Gravity:
    def __init__(self, puzzle_state):
        self.sand_state = None
        self.puzzle_state = puzzle_state
        self.sand_source = np.argwhere(puzzle_state == '+')[0]
        self.current_sand = self.sand_source

    def plot(self, fig=None, ax=None, ax_imshow=None):
        plot_array = np.zeros(self.puzzle_state.shape)
        plot_array[self.puzzle_state == '#'] = 10
        plot_array[self.puzzle_state == 'o'] = 5
        plot_array[self.puzzle_state == '+'] = 1
        if fig is None:
            fig, ax = plt.subplots()
        if ax_imshow is None:
            ax_imshow = ax.imshow(plot_array.T)
        else:
            ax_imshow.set_data(plot_array.T)
        return fig, ax_imshow

    def get_value(self, coord):
        return self.puzzle_state[coord[0], coord[1]]

    def move_one_sand_piece(self):
        # If there is air below sand.. move it?
        below = self.current_sand + np.array([0, 1])
        below_left = self.current_sand + np.array([-1, 1])
        below_right = self.current_sand + np.array([1, 1])

        if self.get_value(below) == '.':
            # We have air
            self.current_sand = below
            self.move_one_sand_piece()
        elif self.get_value(below) == '#' or self.get_value(below) == 'o':
            # We have sand or rock below
            if self.get_value(below_left) == '.':
                self.current_sand = below_left
                self.move_one_sand_piece()
            elif self.get_value(below_right) == '.':
                self.current_sand = below_right
                self.move_one_sand_piece()
            else:
                if self.get_value(self.current_sand) == 'o':
                    return True
                else:
                    self.puzzle_state[self.current_sand[0], self.current_sand[1]] = 'o'
                    self.current_sand = self.sand_source


dfile = os.path.join(DPATH, 'day14')
with open(dfile, 'r') as f:
    puzzle_input = [x.strip() for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if x]



empty_puzzle_cave, correction_coord, max_height = get_blank_cave(puzzle_input=puzzle_input)
filled_puzzle_cave = fill_cave_with_rocks(puzzle_input, empty_puzzle_cave, correction_coord)

gravity_obj = Gravity(filled_puzzle_cave)
gravity_obj.plot()
fig, ax = plt.subplots()
ax_imshow = None
for sand_piece in range(999999):
    gravity_obj.move_one_sand_piece()
    fig, ax_imshow = gravity_obj.plot(fig, ax, ax_imshow=ax_imshow)
    plt.pause(0.01)

"""
Part 2
"""

empty_puzzle_cave, correction_coord, max_height = get_blank_cave(puzzle_input=puzzle_input)
filled_puzzle_cave = fill_cave_with_rocks(puzzle_input, empty_puzzle_cave, correction_coord)
filled_puzzle_cave[:, max_height + 2] = '#'

gravity_obj = Gravity(filled_puzzle_cave)
gravity_obj.plot()
fig, ax = plt.subplots()
ax_imshow = None
for sand_piece in range(999999):
    are_we_done = gravity_obj.move_one_sand_piece()
    if are_we_done:
        break
    # fig, ax_imshow = gravity_obj.plot(fig, ax, ax_imshow=ax_imshow)
    # plt.pause(0.01)

gravity_obj.plot()
