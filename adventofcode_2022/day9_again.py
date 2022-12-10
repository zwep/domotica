import os
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH
import matplotlib.pyplot as plt


"""

"""


def make_a_head_move(head_position, direction_string):
    # Only do single moves so that we track each position properly
    if direction_string == 'R':
        head_position += np.array([1, 0])
    elif direction_string == 'L':
        head_position += np.array([-1, 0])
    elif direction_string == 'U':
        head_position += np.array([0, 1])
    elif direction_string == 'D':
        head_position += np.array([0, -1])
    return head_position


def make_a_tail_move(head_postion, tail_position):
    difference_head_tail = (head_postion - tail_position)
    distance_head_tail = np.sqrt(np.mean((head_postion - tail_position) ** 2))
    # print('Distance before tail move', distance_head_tail)
    # print('Difference before tail move', difference_head_tail)
    # print('Status head ', head_postion)
    # print('Status tail ', tail_position)
    if distance_head_tail > 1:
        # Only do single moves so that we track each position properly
        temp_difference = difference_head_tail / np.abs(difference_head_tail)
        temp_difference[np.isnan(temp_difference)] = 0
        temp_difference = temp_difference.astype(int)
        tail_position += temp_difference

    return tail_position


def process_move(move_string):
    direction_string, step_size = move_string.split()
    step_size = int(step_size)
    return direction_string, step_size


dfile = os.path.join(DPATH, 'day9.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x.strip() for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if x]

# Create global figure/ax
FIG, AX = plt.subplots()
_ = AX.imshow(np.zeros((10, 10)))
plt.grid()
plt.gca().invert_yaxis()
number_of_knots = 10

position_list = [np.array([0, 0]) for _ in range(number_of_knots)]
ax_obj = AX.scatter(*np.array(position_list).T, c='y')

tail_locations = []
for i_move in puzzle_input:
    direction_string, step_size = process_move(i_move)
    for i_step in range(step_size):
        # print(direction_string, i_step)
        tail_locations.append(np.copy(position_list[-1]))
        for ii in range(number_of_knots):
            # print(position_list)
            if ii == 0:
                position_list[ii] = make_a_head_move(head_position=position_list[ii], direction_string=direction_string)
            else:
                position_list[ii] = make_a_tail_move(head_postion=position_list[ii-1], tail_position=position_list[ii])
            #
            # ax_obj.remove()
            # ax_obj = AX.scatter(*np.array(position_list).T, c='y')
            # plt.pause(0.1)

unique_loc = list(set([tuple(x) for x in tail_locations]))
print(len(unique_loc))
plt.scatter(*np.array(unique_loc).T)
