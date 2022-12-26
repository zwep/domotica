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


class ThisRocks:
    def __init__(self, jet_stream):
        self.jet_stream = list(jet_stream)
        self.n_jets = len(self.jet_stream)

        self.landed_coordinates = [(0, 0)]
        self.rock_encyclopedia = {0: [(0, 0), (0, 1), (0, 2), (0, 3)],
                                  1: [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
                                  2: [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
                                  3: [(0, 0), (1, 0), (2, 0), (3, 0)],
                                  4: [(0, 0), (1, 0), (0, 1), (1, 1)]}
        self.n_rocks = len(self.rock_encyclopedia)
        self.max_width = 7
        self.left_offset = 2
        self.bottom_offset = 3

    def initialize_rock(self, current_coordinates):
        return np.array(current_coordinates) + np.array([self.left_offset, self.bottom_offset])

    def falling_motion(self, current_coordinates):
        # Move on down
        # Check with the walls, floor, other rocks
        # Update if necessary
        # Return updated version and if it has landed or not
        new_coordinates = current_coordinates - np.array([0, 1])
        x_coords, y_coords = map(np.array, zip(*new_coordinates))
        if self.check_landed_coords(new_coordinates) or any(y_coords <= 0):
            # We have landed
            return current_coordinates, True
        else:
            # We keep on falling
            return new_coordinates, False

    def check_landed_coords(self, current_coordinates):
        landed_coord_check = [tuple(x) in self.landed_coordinates for x in current_coordinates.tolist()]
        return all(landed_coord_check)

    def jet_motion(self, jet_orientation, current_coordinates):
        # < is to the left
        # > is to the right
        if jet_orientation == '<':
            new_coordinates = current_coordinates + np.array([1, 0])
        elif jet_orientation == '>':
            new_coordinates = current_coordinates + np.array([0, 1])
        else:
            new_coordinates = None
            print('Noooooo')

        x_coords, y_coords = map(np.array, zip(*new_coordinates))
        # Check if it is in within (0, 7) x-coord bounds.
        # And check if it is not hitting any landed block.
        if all(x_coords < self.max_width) and all(x_coords >= 0) and self.check_landed_coords(new_coordinates):
            valid_move = True
        else:
            valid_move = False

        return new_coordinates, valid_move

    def plot(self):
        fig, ax = plt.subplots()
        ax.scatter()

    def run_jets(self, n_landings):
        move_counter = 0
        for landed_items in range(n_landings):
            print(landed_items)
            falling_rock = True
            rock_type = landed_items % self.n_rocks
            init_rock_coords = self.rock_encyclopedia[rock_type]
            current_coordinates = self.initialize_rock(init_rock_coords)
            while falling_rock:
                jet_move = self.jet_stream[move_counter % self.n_jets]
                move_counter += 1
                # self.plot()
                new_coords, valid_motion = self.jet_motion(jet_orientation=jet_move, current_coordinates=current_coordinates)
                if valid_motion is True:
                    current_coordinates = new_coords
                new_coords, falling_rock = self.falling_motion(current_coordinates)
                if falling_rock is True:
                    current_coordinates = new_coords
            self.landed_coordinates.extend([tuple(x) for x in current_coordinates])


puzzle_input_test = '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'
this_rock = ThisRocks(puzzle_input_test)
this_rock.run_jets(2022)
xcoord, ycoord = zip(*this_rock.landed_coordinates)
max(ycoord)

# Test whether we get all the jet streams
# Test if we get all the rocks
# Test if we stop at the right moment