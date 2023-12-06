import numpy as np
import string
import os
import re
import matplotlib.pyplot as plt
from advent_of_code_helper.helper import read_lines_strip, fetch_data, fetch_test_data, int_str2list
from advent_of_code_helper.configuration import DDATA_YEAR


DAY = "5"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = fetch_data(DAY)
_ = fetch_test_data(DAY)

# read input
puzzle_input = read_lines_strip(DDATA_DAY)
test_puzzle_input = read_lines_strip(DDATA_DAY_TEST)

selected_input = puzzle_input

# Process input..
_, str_seed_list = selected_input[0].split(':')
seed_list = int_str2list(str_seed_list)
# New input (puzzle 2)
seed_range_list = [range(seed_source, seed_source + seed_range) for seed_source, seed_range in zip(seed_list[::2], seed_list[1::2])]
sorted_seed_range_list = sorted(seed_range_list, key=lambda x: x.start)

map_collection = {}
value_list = []
key_value = None
for i_line in selected_input[1:] + ['']:
    if (i_line == ''):
        if key_value is not None:
            map_collection.update({key_value: value_list})
        value_list = []
    elif i_line[0] in string.ascii_lowercase:
        key_value = i_line[:-1]
    else:
        value_list.append(i_line)

int_to_map = {i: x for i, x in enumerate(map_collection.keys())}
n_maps = len(int_to_map)

"""Part 1"""
# We need to do the following for each seed
location_list = []
for current_number in seed_list:
    for i_map in range(n_maps):
        map_str = int_to_map[i_map]
        for source_dest_range in map_collection[map_str]:
            dest_int, source_int, range_int = int_str2list(source_dest_range)
            source_range = range(source_int, source_int + range_int)
            dest_range = range(dest_int, dest_int + range_int)
            if current_number in source_range:
                source_index = source_range.index(current_number)
                # Update the current number to the next map
                current_number = dest_range[source_index]
                break

    location_list.append(current_number)

min(location_list)

"""Part 2"""


# Find new interval in next map given current interval
def map_source2dest_interval(a, b, index_map=0):
    # Get the intervals in index_map that overlap (partly) with interval [a,b]
    # BUT DONT FORGET that we need to map the things we dont cover to the same thing
    interval_list = []
    temp_map_str = int_to_map[index_map]
    temp_sorted_map_collection = sorted(map_collection[temp_map_str], key=lambda x: int_str2list(x)[1])
    lowest_source = int_str2list(temp_sorted_map_collection[0])[1]
    temp, int_range = int_str2list(temp_sorted_map_collection[-1])[1:]
    highest_source = temp + int_range
    for jj, temp_interval in enumerate(temp_sorted_map_collection):
        dest_int, source_int, range_int = int_str2list(temp_interval)
        delta = dest_int - source_int
        start_range = max(a, source_int)
        stop_range = min(b, source_int + range_int)
        # Convert it to the destination interval range
        overlap_interval = range(start_range + delta, stop_range + delta)
        interval_list.append(overlap_interval)
    # Only select possible intervals..
    interval_list = list(set([x for x in interval_list if len(x)]))
    if interval_list:
        if a < lowest_source:
            interval_list += [range(a, lowest_source)]
        if highest_source < b:
            interval_list += [range(b, highest_source)]
        return interval_list
    else:
        return [range(a, b)]


def geen_zin_meer_om_te_denken(a, b):
    counter = 0
    x1 = map_source2dest_interval(a, b, counter)
    final_stuff = []
    for x1_range in x1:
        x2 = map_source2dest_interval(x1_range.start, x1_range.stop, counter + 1)
        print(x2)
        for x2_range in x2:
            x3 = map_source2dest_interval(x2_range.start, x2_range.stop, counter + 2)
            for x3_range in x3:
                x4 = map_source2dest_interval(x3_range.start, x3_range.stop, counter + 3)
                for x4_range in x4:
                    x5 = map_source2dest_interval(x4_range.start, x4_range.stop, counter + 4)
                    for x5_range in x5:
                        x6 = map_source2dest_interval(x5_range.start, x5_range.stop, counter + 5)
                        for x6_range in x6:
                            x7 = map_source2dest_interval(x6_range.start, x6_range.stop, counter + 6)
                            final_stuff.extend(x7)
    return sorted(final_stuff, key=lambda x: x.start)

min_location = 99999999999999
for seed_range in sorted_seed_range_list:
    temp = geen_zin_meer_om_te_denken(seed_range.start, seed_range.stop)
    print('\nseed', 'loc')
    # print(seed_range, temp)
    temp_min = min([x.start for x in temp])
    if temp_min < min_location:
        min_location = temp_min
print(min_location)
