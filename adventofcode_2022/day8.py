import os
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH


dfile = os.path.join(DPATH, 'day5.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x for x in f.readlines()]


class ForestView:
    def __init__(self, x_coord, y_coord, puzzle_input):
        self.puzzle_input = puzzle_input
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.value = puzzle_input[x_coord, y_coord]

    def get_top_view(self):
        return puzzle_input[self.x_coord, :self.y_coord]

    def get_bottom_view(self):
        return puzzle_input[self.x_coord, (self.y_coord+1):]

    def get_left_view(self):
        return puzzle_input[:self.x_coord, self.y_coord]

    def get_right_view(self):
        return puzzle_input[(self.x_coord+1):, self.y_coord]

    def get_all_views(self):
        return self.get_top_view(), self.get_bottom_view(), self.get_left_view(), self.get_right_view()

    def get_all_views_reversed(self):
        return self.get_top_view()[::-1], self.get_bottom_view(), self.get_left_view()[::-1], self.get_right_view()

    def calculate_visibility(self):
        view_list = self.get_all_views()
        visibility_list = []
        for i_view in view_list:
            visible_bool = all((self.value - i_view) > 0)
            visibility_list.append(visible_bool)
        return visibility_list

    def calculate_scenic_score(self):
        view_reversed_list = self.get_all_views_reversed()
        scenic_score_list = []
        for i_view in view_reversed_list:
            if len(i_view):
                larger_tree_bool = list(i_view >= self.value)
                if True in larger_tree_bool:
                    max_view = larger_tree_bool.index(True) + 1
                else:
                    max_view = len(larger_tree_bool)
            else:
                max_view = 0
            scenic_score_list.append(max_view)
        return scenic_score_list

    def print(self):
        top_view, bottom_view, left_view, right_view = self.get_all_views()
        print('Top view', top_view)
        print('Bottom view', bottom_view)
        print('Left view', left_view)
        print('Right view', right_view)


dfile = os.path.join(DPATH, 'day8.txt')
with open(dfile, 'r') as f:
    puzzle_input = [list(map(int, list(x.strip()))) for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if x]
puzzle_input = np.array(puzzle_input)
n_size, _ = puzzle_input.shape

object_list = []

for i in range(1, n_size-1):
    for j in range(1, n_size-1):
        print(i, j)
        forest_object = ForestView(x_coord=i, y_coord=j, puzzle_input=puzzle_input)
        position_visibility = forest_object.calculate_visibility()
        if any(position_visibility):
            object_list.append(forest_object)

len(object_list) + 2 * n_size + 2 * (n_size - 2)

scenic_scores = []
for i in range(0, n_size):
    for j in range(0, n_size):
        # print(i, j)
        forest_object = ForestView(x_coord=i, y_coord=j, puzzle_input=puzzle_input)
        scenic_score = forest_object.calculate_scenic_score()
        scenic_scores.append(np.prod(scenic_score))

max(scenic_scores)
