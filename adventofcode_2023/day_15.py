import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def HASH_algorithm(current_value, sel_str):
    current_value += ord(sel_str)
    current_value *= 17
    current_value %= 256
    return current_value


def HASH_string(x_str):
    current_value = 0
    for x in list(x_str):
        current_value = HASH_algorithm(current_value, x)
    return current_value


DAY = "15"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)


"""
test case
"""

for i_line in puzzle_input:
    s = 0
    for i_str in i_line.split(","):
        res = HASH_string(i_str)
        s += res

print(s)
""" 
Part 2

Example rn=1

Each step begins with a sequence of letters that indicate the label of the lens on which the step operates. 'rn'

The result of running the HASH algorithm on the label indicates the correct box for that step  HASH_string('rn') = 0

The label will be immediately followed by a character that indicates the operation to perform: 
either an equals sign (=) or a dash (-). --> =

If the operation character is a dash (-), go to the relevant box and remove the lens with the given label if it is present in the box. 
Then, move any remaining lenses as far forward in the box as they can go without changing their order, filling any space made by removing the indicated lens. 
(If no lens in that box has the given label, nothing happens.)

If the operation character is an equals sign (=), it will be followed by a number indicating the focal length of the lens that needs to go into the relevant box; 
be sure to use the label maker to mark the lens with the label given in the beginning of the step so you can find it later. 
There are two possible situations:

    If there is already a lens in the box with the same label, replace the old lens with the new lens: 
        remove the old lens and put the new lens in its place, not moving any other lenses in the box. (SO update the focal length...?)
    If there is not already a lens in the box with the same label, add the lens to the box immediately behind any lenses already in the box. 
        Don't move any of the other lenses when you do this. If there aren't any lenses in the box, the new lens goes all the way to the front of the box.

"""

box_collection = {}
for i_line in puzzle_input:
    for i_str in i_line.split(","):
        if '=' in i_str:
            label, focal_length = i_str.split('=')
        else:  # '-' in i_str:
            label, _ = i_str.split('-')

        box_number = HASH_string(label)
        box_number_key = f'box_{box_number}'
        _ = box_collection.setdefault(box_number_key, ([], []))
        # Go to the box..
        label_list, focal_length_list = box_collection[box_number_key]
        # Decide what to do
        if '=' in i_str:
            """            
            If there is already a lens in the box with the same label, replace the old lens with the new lens: 
                remove the old lens and put the new lens in its place, not moving any other lenses in the box. (SO update the focal length...?)
            If there is not already a lens in the box with the same label, add the lens to the box immediately behind any lenses already in the box. 
                Don't move any of the other lenses when you do this. If there aren't any lenses in the box, the new lens goes all the way to the front of the box.
            """
            if label in label_list:
                index_label = label_list.index(label)
                focal_length_list[index_label] = focal_length
            else:
                label_list.append(label)
                focal_length_list.append(focal_length)
        else:
            """            
            If the operation character is a dash (-), go to the relevant box and remove the lens with the given label if it is present in the box. 
            Then, move any remaining lenses as far forward in the box as they can go without changing their order, filling any space made by removing the indicated lens. 
            (If no lens in that box has the given label, nothing happens.)
            """
            if label in label_list:
                index_label = label_list.index(label)
                label_list.pop(index_label)
                focal_length_list.pop(index_label)
        # print(box_collection)
        for k in sorted(box_collection, key=lambda x: int(x.split('_')[1])):
            v = box_collection[k]
            if len(v[0]):
                print(k, [v[0][jj] + v[1][jj] for jj in range(len(v[0]))])
        print('---')

# 152..?
s = 0
for k, v in box_collection.items():
    box_int = int(k.split('_')[-1])
    temp_label, temp_f_l = v
    if len(temp_f_l):
        for ii, f_l in enumerate(temp_f_l):
            s += (box_int + 1) * (ii + 1) * int(f_l)

print(s)

# 10448 - too low