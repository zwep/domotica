import re
import numpy as np

import itertools
import collections


def get_bin_numbers(B):
    intAB = int(''.join(B[0, :]), 2)
    intBA = int(''.join(B[0, ::-1]), 2)
    intBD = int(''.join(B[:, 0]), 2)
    intDB = int(''.join(B[::-1, 0]), 2)

    intDC = int(''.join(B[-1, :]), 2)
    intCD = int(''.join(B[-1, ::-1]), 2)
    intBC = int(''.join(B[:, -1]), 2)
    intCB = int(''.join(B[::-1, -1]), 2)

    sides = [intAB, intBA, intBD, intDB, intDC, intCD, intBC, intCB]
    return sides


def find_tile_from_value(value_list, tile_numbers):
    tile_dict = {}
    for i_value in value_list:
        for k, v in tile_numbers.items():
            # We relate the value to the current tile.
            if i_value in v:
                tile_dict.setdefault(k, [])
                tile_dict[k].append(i_value)
    return tile_dict


day = 20
with open(f"adventofcode_2020/day{str(day)}_numbers.txt", "r") as f:
    A = f.read().splitlines()

A = [re.sub("#", "1", x) for x in A]
A = [re.sub("\.", "0", x) for x in A]

# Read in all the data and create list of dicts (Tile: tile_values)
tile_list = []
tile_index = [i for i, x in enumerate(A) if 'Tile' in x]
for i in range(len(tile_index)):
    i_tile_index = tile_index[i]
    if i+1 >= len(tile_index):
        j_tile_index = None
    else:
        j_tile_index = tile_index[i+1] - 1
    temp_dict = {A[i_tile_index]: [list(x) for x in A[i_tile_index+1:j_tile_index]]}
    tile_list.append(temp_dict)

# Calculate all possible sides in binary format
tile_numbers = {}
for i_tile in tile_list:
    temp_dict = {}
    for k, v in i_tile.items():
        B = np.array(v)
        side_numbers = get_bin_numbers(B)
        temp_dict[k] = side_numbers

    tile_numbers.update(temp_dict)


list_of_tile_values = list(tile_numbers.values())
list_of_tile_values_concat = list(itertools.chain(*list_of_tile_values))
# These boundary values only exist once...
# And hence belong to the boundary (because they are unique)
unique_boundary_values = [k for k, v in collections.Counter(list_of_tile_values_concat).items() if v == 1]
unique_boundary_dict = find_tile_from_value(unique_boundary_values, tile_numbers)

s0 = 1
for k, v in unique_boundary_dict.items():
    if len(v) == 4:
        found_tile = int(re.findall("[0-9]{4}", k)[0])
        print(found_tile)
        s0 *= found_tile

print('Asnwer to part 1 ', s0)

"""
Part 2..
"""

tile_position = []
matched_boundary_dict = {}
# Starting with a corner..
sel_tile_key = 'Tile 1951:'
tile_position.append(sel_tile_key)

# Gets the outer rows...
while True:
    tile_values = tile_numbers[sel_tile_key]
    tile_outside_values = unique_boundary_dict[sel_tile_key]
    tile_matched_values = matched_boundary_dict.get(sel_tile_key, [])

    exclude_values = set(tile_outside_values).union(set(tile_matched_values))
    tile_inside_boundaries = list(set(tile_values).difference(exclude_values))

    unique_inside_boundary_dict = find_tile_from_value(tile_inside_boundaries, tile_numbers)
    unique_inside_boundary_dict = {k: v for k, v in unique_inside_boundary_dict.items() if k not in tile_position}
    unique_inside_boundary_dict = {k: v for k, v in unique_inside_boundary_dict.items() if k in unique_boundary_dict.keys()}

    # Very wrong I guess...
    if len(unique_inside_boundary_dict) == 0:
        break

    # Choose one key...?
    sel_tile_key_neighbour = list(unique_inside_boundary_dict.keys())[0]
    matched_value = unique_inside_boundary_dict[sel_tile_key_neighbour]
    matched_boundary_dict.setdefault(sel_tile_key_neighbour, [])
    matched_boundary_dict[sel_tile_key_neighbour].extend(matched_value)
    matched_boundary_dict.setdefault(sel_tile_key, [])
    matched_boundary_dict[sel_tile_key].extend(matched_value)

    tile_position.append(sel_tile_key_neighbour)
    print(tile_position)
    sel_tile_key = tile_position[-1]

# Also add the last pair of values...
first_key = tile_position[0]
last_key = tile_position[-1]
matched_value = list(set(tile_numbers[first_key]).intersection(set(tile_numbers[last_key])))
matched_boundary_dict[first_key].extend(matched_value)
matched_boundary_dict[last_key].extend(matched_value)

for k, v in matched_boundary_dict.items():
    print(k, v)

# Somewhere I need to figure out how to repeat all this...
# But I also need to order everything
inner_tiles = {k: v for k, v in tile_numbers.items() if k not in matched_boundary_dict.keys()}
if len(inner_tiles) == 1:
    print('We are done')

# Redo something from above. Get all the current tile values
list_of_tile_values = list(tile_numbers.values())
list_of_tile_values_concat = list(itertools.chain(*list_of_tile_values))
# Remove the current matches values
list_of_matched_tile_values = list(matched_boundary_dict.values())
list_of_matched_tile_values_concat = list(itertools.chain(*list_of_matched_tile_values))

remaining_tile_values = list(set(list_of_tile_values_concat).difference(set(list_of_matched_tile_values_concat)))

unique_boundary_values = [k for k, v in collections.Counter(remaining_tile_values).items() if v == 1]
unique_boundary_dict = find_tile_from_value(unique_boundary_values, tile_numbers)

# Reorder the result....

def get_coordinates(i, n_grid):
    n_amount = n_grid - 2*i
    x = [i] * (n_amount - 1) + list(range(i, n_grid-(i+1))) + [n_grid-i-1] * (n_amount-1) + list(range(n_grid-(i+1), i, -1))
    y = list(range(i, n_grid-(i+1))) + [n_grid-i-1] * (n_amount-1) + list(range(n_grid-(i+1), i, -1)) + [i] * (n_amount - 1)
    return list(zip(x, y))


n_tiles = len(tile_numbers)
n_grid = int(np.sqrt(n_tiles))
image_array = np.zeros((8 * n_grid, 8 * n_grid), dtype=str)
map_to_array = get_coordinates(0, n_grid)

processed_tiles = []
for i_tile in tile_list:
    for k, v in i_tile.items():
        if k in tile_position:
            index_tile = tile_position.index(k)
            jj, ii = map_to_array[index_tile]
            A_sub = np.array(v)[1:-1, 1:-1]
            image_array[ii*8: (ii+1) * 8, jj*8:(jj+1)*8] = A_sub
            processed_tiles.append(k)

remaining_tiles = list(set([list(x.keys())[0] for x in tile_list]).difference(set(processed_tiles)))
tile_dict = {list(x.keys())[0]: list(x.values()) for x in tile_list}
last_tile_values = tile_dict[remaining_tiles[0]]
# Add the middle one....
ii, jj = (n_grid//2, n_grid//2)
A_sub = np.array(last_tile_values)[0, 1:-1, 1:-1]
image_array[ii*8: (ii+1) *8, jj*8:(jj+1)*8] = A_sub

import matplotlib.pyplot as plt
plt.imshow(image_array.astype(int))