import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def update_position(cur_pos, delta_pos):
    return [cur_pos[0] + delta_pos[0], cur_pos[1] + delta_pos[1]]


def run_part_1(starting_position, starting_direction):
    position_direction_stack = [(starting_position, starting_direction)]
    memory = []
    while len(position_direction_stack):
        current_position, current_direction = position_direction_stack.pop()
        # Maybe this is useful..?
        cur_line, cur_col = current_position
        # Stop if we are out of bounds
        if (cur_line < 0) or (cur_line >= max_line) or (cur_col < 0) or (cur_col >= max_col):
            continue

        if (current_position + [current_direction]) in memory:
            continue

        current_tile = selected_input[cur_line][cur_col]
        memory.append(current_position + [current_direction])
        """
        I could but the code below in a function
        But I do not see a benefit yet
        """
        # Nothing special happens
        if current_tile == '.':
            delta_pos = direction2pos[current_direction]
            next_position = update_position(current_position, delta_pos)
            position_direction_stack.append((next_position, current_direction))
        # Now we need to split...
        elif current_tile == '|':
            # Now we are going to move in two directions..
            if (current_direction == 'E') or (current_direction == 'W'):
                for new_direction in ['N', 'S']:
                    delta_pos = direction2pos[new_direction]
                    next_position = update_position(current_position, delta_pos)
                    position_direction_stack.append((next_position, new_direction))
            # Keep going... (if South or North)
            else:
                delta_pos = direction2pos[current_direction]
                next_position = update_position(current_position, delta_pos)
                position_direction_stack.append((next_position, current_direction))
        elif current_tile == '-':
            # Now we are going to move in two directions..
            if (current_direction == 'N') or (current_direction == 'S'):
                for new_direction in ['E', 'W']:
                    delta_pos = direction2pos[new_direction]
                    next_position = update_position(current_position, delta_pos)
                    position_direction_stack.append((next_position, new_direction))
            # Keep going... (if South or North)
            else:
                delta_pos = direction2pos[current_direction]
                next_position = update_position(current_position, delta_pos)
                position_direction_stack.append((next_position, current_direction))
        elif current_tile == '/':
            # Rotate direction
            new_direction = direction2rot45[current_direction]
            delta_pos = direction2pos[new_direction]
            next_position = update_position(current_position, delta_pos)
            position_direction_stack.append((next_position, new_direction))
        elif current_tile == '\\':
            # Rotate direction
            new_direction = direction2rot135[current_direction]
            delta_pos = direction2pos[new_direction]
            next_position = update_position(current_position, delta_pos)
            position_direction_stack.append((next_position, new_direction))

    # Print the path...?
    display_path = []
    for i_line in range(max_line):
        temp = ' ' * max_col
        display_path.append(temp)

    for i_mem in memory:
        i_line, i_col, i_dir = i_mem
        temp = list(display_path[i_line])
        temp[i_col] = '#'
        display_path[i_line] = ''.join(temp)

    # The answer and for display.. super fun
    return ''.join(display_path).count('#'), display_path



direction2pos = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1]}
# pos2inverse = {'S': 'N', 'E': 'W', 'W': 'E', 'N': 'S', None: 'None'}
direction2rot45 = {'S': 'W', 'E': 'N', 'W': 'S', 'N': 'E', None: 'None'}
direction2rot135 = {'S': 'E', 'E': 'S', 'W': 'N', 'N': 'W', None: 'None'}



DAY = "16"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)
selected_input = puzzle_input

max_col = len(selected_input[0])
max_line = len(selected_input)

# Letsee gooo
starting_index = [0, 0]
start_direction = 'E'
# SO here we store locations for splitters..?
# Or do it in a tuple?
# direction_stack = []
import time
t0 = time.time()
result, _ = run_part_1(starting_index, start_direction)
print(time.time() - t0)

"""
Part 2

Bruteforce will takequite some time (5 minutes approx)
"""
# This is all the West boundaries
result_west = []
starting_direction = 'E'
temp = list(zip(range(max_line), [0] * max_line))
for ii, starting_pos in enumerate(temp):
    print(f'{ii}/{len(temp)}', end='\r')
    result, _ = run_part_1(list(starting_pos), starting_direction)
    result_west.append(result)

result_east = []
starting_direction = 'W'
temp = list(zip(range(max_line), [max_col - 1] * max_line))
for ii, starting_pos in enumerate(temp):
    print(f'{ii}/{len(temp)}', end='\r')
    result, _ = run_part_1(list(starting_pos), starting_direction)
    result_east.append(result)

# North side
result_north = []
starting_direction = 'S'
temp = list(zip([0] * max_col, range(max_col)))
for ii, starting_pos in enumerate(temp):
    print(f'{ii}/{len(temp)}', end='\r')
    result, _ = run_part_1(list(starting_pos), starting_direction)
    result_north.append(result)

result, _ = run_part_1(list(temp[3]), 'S')

# South side
result_south = []
starting_direction = 'N'
temp = list(zip([max_line - 1] * max_col, range(max_col)))
for ii, starting_pos in enumerate(temp):
    print(f'{ii}/{len(temp)}', end='\r')
    result, _ = run_part_1(list(starting_pos), starting_direction)
    result_south.append(result)

max(max(max(result_south), max(result_north)), max(max(result_west), max(result_east)))


"""
Now try some memoization...?

Other stuff to do
"""
# result, _ = run_part_1(list(starting_pos), starting_direction)