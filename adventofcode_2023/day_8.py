import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR

# Convert to dict
def get_mapping(puzzle_input):
    source2dest = {}
    for x in puzzle_input:
        source, dest_tuple = x.split('=')
        dest_L, dest_R = re.sub('\(|\)', '', dest_tuple).strip().split(', ')
        source2dest[source.strip()] = [dest_L, dest_R]
    return source2dest


DAY = "8"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

selected_puzzle_input = puzzle_input
# Generic..
command = selected_puzzle_input[0]
source2dest = get_mapping(selected_puzzle_input[2:])
LR2int = {'L': 0, 'R': 1}

"""
Part 1
"""

underway = True
command_counter = 0
step_counter = 0
len_command = len(command)
position = 'AAA'
while underway:
    print(position, command_counter)
    step_counter += 1
    sel_command = command[command_counter]
    sel_index = LR2int[sel_command]
    position = source2dest[position][sel_index]
    command_counter = (command_counter + 1) % len_command
    if position == 'ZZZ':
        break

print(step_counter)

"""
Part 2
"""

# Check if nodes end with Z
def are_we_there_yet(position_list):
    return all([x.endswith('Z') for x in position_list])

def get_cycle_attr(sel_position):
    command_counter = 0  # Used for the commands..
    step_counter = 0  # Used for the final answer
    len_command = len(command)
    starting_position = sel_position
    sel_cycle_dict = {sel_position: {}}
    start_the_cycle = True
    while start_the_cycle:
        step_counter += 1
        sel_command = command[command_counter]
        sel_index = LR2int[sel_command]
        # Update the position
        sel_position = source2dest[sel_position][sel_index]
        # Check if it ends with Z
        if sel_position.endswith('Z'):
            _ = sel_cycle_dict[starting_position].setdefault(sel_position, [])
            temp_cycle_list = sel_cycle_dict[starting_position][sel_position]
            n_cycles = len(temp_cycle_list)
            # If we have something...
            if n_cycles:
                cycle_counter = 0
                for i_cycle in temp_cycle_list:
                    if (step_counter % i_cycle) == 0:
                        cycle_counter += 1
                        continue
                    else:
                        sel_cycle_dict[starting_position][sel_position].append(step_counter)
                if cycle_counter == n_cycles:
                    start_the_cycle = False
            else:
                sel_cycle_dict[starting_position][sel_position].append(step_counter)
        command_counter = (command_counter + 1) % len_command
    return sel_cycle_dict


# Define generic stuff again
selected_puzzle_input = puzzle_input
command = selected_puzzle_input[0]
source2dest = get_mapping(selected_puzzle_input[2:])
LR2int = {'L': 0, 'R': 1}

# Get starting nodes
position_list = [x for x in source2dest.keys() if x.endswith('A')]

uber_cycle_dict = {}
for sel_position in position_list:
    temp_dict = get_cycle_attr(sel_position)
    uber_cycle_dict.update(temp_dict)

# Copied the values, because getting them from a nested dict is mildly annoying
found_cycles = [18961, 12169, 17263, 13301, 14999, 16697]
import math
num1 = found_cycles[0]
num2 = found_cycles[1]
lcm = math.lcm(num1, num2)

for i in range(2, len(found_cycles)):
    lcm = math.lcm(lcm, found_cycles[i])

print(lcm)

lcm / len(command)