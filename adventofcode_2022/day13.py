import os
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH
import matplotlib.pyplot as plt
import string
import itertools


def process_input(puzzle_input):
    puzzle_pairs = []
    temp_list = []
    for i_item in puzzle_input:
        i_item = i_item.strip()
        if i_item != '':
            result = eval(i_item)
            temp_list.append(result)
        else:
            puzzle_pairs.append(temp_list)
            temp_list = []
    puzzle_pairs.append(temp_list)
    return puzzle_pairs


def process_input_part2(puzzle_input):
    puzzle_list = []
    for i_item in puzzle_input:
        i_item = i_item.strip()
        if i_item != '':
            result = eval(i_item)
            puzzle_list.append(result)
    return puzzle_list


class CompareItems:
    def __init__(self, left_item, right_item, debug=False):
        self.left_item = left_item
        self.right_item = right_item
        self.status = None
        self.debug = debug

    def compare_items(self, x=None, y=None):
        if self.status is not None:
            return self.status

        if x is None:
            x = self.left_item
        if y is None:
            y = self.right_item

        if self.debug:
            print('Left item ', x, 'Right item', y)

        # How am I going to store the results..?
        x, y, item_type = self.homogenize_items(x, y)
        if item_type:
            n_x = len(x)
            n_y = len(y)
            counter = 0
            #
            for i in range(min(n_x, n_y)):
                counter += 1
                result = self.compare_items(x[i], y[i])
                # If we have one positive result, we are OK
                if result is not None:
                    self.status = result

            if self.status is None:
                if n_x == n_y:
                    self.status = None
                elif counter == n_x:
                    self.status = True
                elif counter == n_y:
                    #  If the right list runs out of items first, the inputs are not in the right order.
                    self.status = False
        else:
            return self.compare_integers(x, y)

    @staticmethod
    def homogenize_items(x, y):
        if isinstance(x, list) and isinstance(y, list):
            return x, y, 1
        elif isinstance(x, int) and isinstance(y, int):
            return x, y, 0
        elif isinstance(x, int) and isinstance(y, list):
            return [x], y, 1
        elif isinstance(x, list) and isinstance(y, int):
            return x, [y], 1

    @staticmethod
    def compare_integers(x, y):
        if x < y:
            return True
        elif x > y:
            return False
        else:
            return None


dfile = os.path.join(DPATH, 'day13.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x for x in f.readlines()]


puzzle_input = [x for x in puzzle_input if x]
puzzle_pairs = process_input(puzzle_input)
puzzle_pairs = [x for x in puzzle_pairs if len(x) == 2]
puzzle_states = []
for ii, (x, y) in enumerate(puzzle_pairs):
    print(f'=============== {ii} ================')
    compare_obj = CompareItems(x, y, debug=True)
    compare_obj.compare_items()
    if compare_obj.status:
        puzzle_states.append(True)
    else:
        puzzle_states.append(False)

    print('Puzzle state ', puzzle_states[ii])

"""
Part 2..
"""

dfile = os.path.join(DPATH, 'day13_part2.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if x]
puzzle_list = process_input_part2(puzzle_input)

def compare(x, y):
    compare_obj = CompareItems(x, y, debug=True)
    compare_obj.compare_items()
    return 2 * int(compare_obj.status) - 1

import functools
puzzle_list.sort(key=functools.cmp_to_key(compare))
puzzle_list = puzzle_list[::-1]

[i for i, x in enumerate(puzzle_list) if x == [[2]] or x == [[6]]]
