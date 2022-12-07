import os
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH


def extract_crates(single_line, max_col):
    temp_crates = [''] * max_col
    for ii in range(max_col):
        i_crate = single_line[ii * 4:(ii + 1) * 4]
        i_crate = re.sub('\[|\]', '', i_crate).strip()
        temp_crates[ii] = i_crate
    return temp_crates


def change_list_order(list_format):
    # and vica versa
    new_format = [[] for _ in range(len(list_format[0]))]
    for i in list_format:
        for ii, j in enumerate(i):
            if j:
                new_format[ii].append(j)
    return new_format


def process_move(crate_list, move_ind, from_ind, to_ind):
    for i_move in range(move_ind):
        loose_crate = crate_list[from_ind].pop()
        crate_list[to_ind].extend(loose_crate)
    return crate_list


def process_move_part2(crate_list, move_ind, from_ind, to_ind):
    loose_crates = crate_list[from_ind][-move_ind:]
    del crate_list[from_ind][-move_ind:]
    crate_list[to_ind].extend(loose_crates)
    return crate_list


dfile = os.path.join(DPATH, 'day5.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x for x in f.readlines()]

split_index = [i for i, x in enumerate(puzzle_input) if x == '\n']
i_split = split_index[0]
# Process crates
crates_input = puzzle_input[:i_split]
col_length = crates_input.pop()
col_num_list = [int(x) for x in col_length.strip().split()]
max_col = max(col_num_list)

crate_list = []
for i_line in crates_input:
    temp_crate = extract_crates(i_line, max_col)
    crate_list.append(temp_crate)

# Flip the list of list...
crate_list_flipped = change_list_order(crate_list[::-1])

"""
Part 1
"""

def part1():
    global crate_list_flipped
    move_orders = puzzle_input[(i_split+1):-1]
    for i_line in move_orders:
        print(i_line)
        move_ind, from_ind, to_ind = map(int, re.findall('move ([0-9]*) from ([0-9])* to ([0-9])', i_line.strip())[0])
        crate_list_flipped = process_move(crate_list_flipped, move_ind, from_ind-1, to_ind-1)

    print(''.join([x[-1] for x in crate_list_flipped]))

"""
Part 2
"""

def part2():
    global crate_list_flipped
    move_orders = puzzle_input[(i_split+1):-1]
    for i_line in move_orders:
        print(i_line)
        move_ind, from_ind, to_ind = map(int, re.findall('move ([0-9]*) from ([0-9])* to ([0-9])', i_line.strip())[0])
        crate_list_flipped = process_move_part2(crate_list_flipped, move_ind, from_ind-1, to_ind-1)

    print(''.join([x[-1] for x in crate_list_flipped]))

if __name__ == "__main__":
    part1()
    part2()