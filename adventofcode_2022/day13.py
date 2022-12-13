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


class CompareItems:
    def __init__(self, left_item, right_item, debug=False):
        self.left_item = left_item
        self.right_item = right_item
        self.status = []
        self.debug = debug

    def compare_items(self, x=None, y=None):
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
            #result = False
            for i in range(max(n_x, n_y)):
                if i >= n_x:
                    # If the left list runs out of items first, the inputs are in the right order.
                    self.status.append(True)
                    break
                if i >= n_y:
                    #  If the right list runs out of items first, the inputs are not in the right order.
                    self.status.append(False)
                    break
                result = self.compare_items(x[i], y[i])
                self.status.append(result)

        else:
            result = self.compare_integers(x, y)
            # Zoiets..?
            self.status.append(result)

        if False in self.status:
            return

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
            return -1



dfile = os.path.join(DPATH, 'day13.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if x]
puzzle_pairs = process_input(puzzle_input)
puzzle_states = []
for ii, (x, y) in enumerate(puzzle_pairs):
    print(f'=============== {ii} ================')
    if ii <100:
        compare_obj = CompareItems(x, y, debug=True)
        compare_obj.compare_items()
        if False in compare_obj.status:
            puzzle_states.append(False)
        else:
            puzzle_states.append(True)

        print('Puzzle state ', puzzle_states[ii])


    # It should be..
    # [True, True, False, True, False, True, False, False]