import os
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH
import matplotlib.pyplot as plt
import string
import itertools


class FindRoute:
    def __init__(self, puzzle_input, current_location):
        self.puzzle_input = puzzle_input
        self.n_size, _ = self.puzzle_input.shape
        self.start_loc = np.argwhere(self.puzzle_input == 'S')[0]
        self.final_loc = np.argwhere(self.puzzle_input == 'E')[0]
        self.current_loc = current_location
        self.current_elevation = self.puzzle_input[self.current_loc]
        self.possible_directions = [[1, 0], [-1, 0], [0, -1], [0, 1]]
        self.translator = dict(zip(list(string.ascii_lowercase), list(range(len(string.ascii_lowercase)))))
        self.states = list(itertools.product(range(self.n_size), range(self.n_size)))
        self.states_dict = dict(zip(self.states, [np.inf for _ in range(len(self.states))]))
        # Delete the starting location ?
        del self.states_dict[tuple(self.start_loc)]

    def allowed_directions(self):
        # Look up
        allowed_directions = []
        for i_direction in self.possible_directions:
            temp_location = self.current_loc + np.array(i_direction)
            if all(temp_location >= 0) and all(temp_location < self.n_size):
                print(f'Looking at location {i_direction}')
                if np.abs(self.translator[self.current_elevation] - self.translator[self.puzzle_input[temp_location[0], temp_location[1]]]) <= 1:
                    allowed_directions.append(i_direction)
        return allowed_directions

    def take_a_step(self):
        for i_direction in self.allowed_directions():
            temp_location = self.current_loc + np.array(i_direction)


def process_input(x):
    pass



dfile = os.path.join(DPATH, 'day12.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x.strip() for x in f.readlines()]

puzzel_array = np.array([list(x) for x in puzzle_input])
find_route_obj = FindRoute(puzzle_input=puzzel_array)
find_route_obj.allowed_directions()



