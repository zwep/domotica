import itertools

import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR

"""
# Too high 27869
"""


def get_part_1(selected_puzzle):
    pool = [[0, 0]]

    for i_line in selected_puzzle:
        current_position = pool[-1]
        direction, step_size, edge_color = i_line.split()
        step_size = int(step_size)
        delta_x, delta_y = helper.STEP2POS[direction]
        for i_step in range(0, step_size + 1):
            new_position = helper.update_position(current_position, [delta_x * i_step, delta_y * i_step])
            pool.append(new_position)
    return pool


def get_range(max_points, line_points):
    range_list = []
    start_range = 0
    for ii in range(max_points):
        # Check if points ii-1, ii, or ii+1 is in the boundary points
        prev = ii - 1 in line_points
        curr = ii in line_points
        next = ii + 1 in line_points
        if curr is False:
            continue  # Dont add
        else:
            if prev is False and next is False:
                # Boundary...
                temp = range(start_range+1, ii)
                range_list.append(temp)
                start_range = ii
            elif prev is False and next is True:
                # Start of a block..
                temp = range(start_range+1, ii)
                range_list.append(temp)
                # start_range = ii
            elif prev is True and next is False:
                # End of a block
                # temp = range(start_range, ii)
                # range_list.append(temp)
                start_range = ii
            elif prev is True and next is True:
                pass
                #print('Inside a block ', ii)
            else:
                print('Derp', ii)
    else:
        temp = range(start_range + 1, max_points)
        range_list.append(temp)
    return range_list


def get_inside_ranges(row_range, row_prev, row_next):
    """
    The intervals were based on the following idea

    [.....)#[....)###[....)#[.....)

    :param row_range:
    :param row_prev:
    :param row_next:
    :return:
    """
    if len(row_range) <= 2:
        return []
    res = {}
    for i, i_range in enumerate(row_range):
        counter = 0
        # The first interval is always done
        # Same for the last interval..
        if i == 0:
            res[i] = counter
            continue
        else:
            # Get the previous count...
            # If the distance with the previous range is one..
            # Then we simply need to add 1 from that previous count...
            if (i_range.start - row_range[i-1].stop) == 1:
                res[i] = res[i-1] + 1
                continue
            cur_thing = i_range.stop
            for j_range in row_range[i + 1:]:
                if j_range.start - cur_thing == 1:
                    counter += 1
                elif j_range.start - cur_thing > 1:
                    if ((cur_thing) in row_prev) != ((j_range.start-1) in row_next):
                        counter += 0
                    else:
                        counter += 1

                else:
                    print('no clue', cur_thing, i_range, j_range, row_range)
                cur_thing = j_range.stop
            # If all the intervals are processed, store the result
            else:
                res[i] = counter

    inside_point = []
    for k, v in res.items():
        if v % 2 == 1:
            inside_point.extend(row_range[k])

    return inside_point


def get_inside_points(pool):
    max_pool_x = pool[:, 0].max() + 5
    max_pool_y = pool[:, 1].max() + 5

    inside_point_list = []
    for i_row in range(max_pool_x):
        pool_row = sorted([x[1] for x in pool if x[0] == i_row])
        pool_row_prev = sorted([x[1] for x in pool if x[0] == i_row - 1])
        pool_row_next = sorted([x[1] for x in pool if x[0] == i_row + 1])
        row_range = get_range(max_pool_y, pool_row)
        temp_inside_point = get_inside_ranges(row_range, pool_row_prev, pool_row_next)
        inside_point_list.append(temp_inside_point)
    return inside_point_list


get_left = {'N': 'W', 'E': 'N', 'S': 'E', 'W': 'S'}
get_right = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
# 0 means R, 1 means D, 2 means L, and 3 means U
convert_int_to_dir = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}

DAY = "18"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

selected_puzzle = puzzle_input

# Part 1
pool = get_part_1(selected_puzzle)

#
# Correct for minus...
min_x_pos = abs(min(np.array(pool)[:, 0].min(), np.array(pool)[:, 0].min())) + 2
min_y_pos = abs(min(np.array(pool)[:, 1].min(), np.array(pool)[:, 1].min())) + 2
pool_array = np.array([helper.update_position(x, [min_x_pos, min_y_pos]) for x in pool])

inside_point_list = get_inside_points(pool_array)
print(sum([len(x) for x in inside_point_list]) + len(set([tuple(x) for x in pool])))


"""Visualize what we are doing only for part 1"""
# Create the path...
max_pool_x = pool_array[:, 0].max() + 5
max_pool_y = pool_array[:, 1].max() + 5
A = np.zeros((max_pool_x+2, max_pool_y+2))
for ix, iy in pool_array:
    A[ix, iy] = 2

for ii, jj_list in enumerate(inside_point_list):
    if len(jj_list):
        for jj in jj_list:
            A[ii, jj] += 0.5

plt.imshow(A)

"""
Part 2

"""

selected_puzzle = puzzle_input

pool_part2 = [[0, 0]]
wall_distance = 0
vertex_list = []
for i_line in selected_puzzle:
    # direction, step_size, edge_color = i_line.split()
    # step_size = int(step_size)
    # delta_x, delta_y = helper.STEP2POS[direction]
    _, _, edge_color = i_line.split()
    edge_color = edge_color[1:-1]
    direction = convert_int_to_dir[edge_color[-1]]
    step_size = int(edge_color[1:-1], 16)
    print(step_size)
    delta_x, delta_y = helper.STEP2POS[direction]
    current_position = pool_part2[-1]
    new_position = helper.update_position(current_position, [delta_x * step_size, delta_y * step_size])
    pool_part2.append(new_position)
    wall_distance += step_size
    x_start = current_position[0]
    x_stop = current_position[0] + delta_x * step_size
    step_dir = 1 if x_start < x_stop else -1
    x_range = range(x_start, x_stop + step_dir, step_dir)
    y_start = current_position[1]
    y_stop = current_position[1] + delta_y * step_size
    step_dir_y = 1 if y_start < y_stop else -1
    y_range = range(y_start, y_stop + step_dir_y, step_dir_y)
    vertex_list.append((x_range, y_range))


# len(pool_part2)
min_x = min([x[0] for x in pool_part2]) - 20
min_y = min([x[1] for x in pool_part2]) - 20
max_x = max([x[0] for x in pool_part2]) + 20
max_y = max([x[1] for x in pool_part2]) + 20
# A = np.zeros(((max_x - min_x), (max_y - min_y)))
# for i_pool in pool_part2:
#     ix, iy = i_pool
#     A[ix + abs(min_x), iy + abs(min_y)] += 1
#
# plt.imshow(A)

"""
Okay so now we got only the corner coordinates...

Now what...
Well... we can define the patches...
"""


def get_other_coords(sel_x, sel_y, ordered_x_coord, ordered_y_coord):
    # Given two grid coords selx and sely.. check if we encounter any PATH coords when we move forward..
    # If not... well, then nobody cares
    # If we DO!  Then we can, and need to check if it is inside or not
    # What we return is a list of coords..
    # Where we return the two coords that are "after" the given x coord
    # And the given y-coord is exactly between these points
    found_points = []
    for i, iy in enumerate(ordered_y_coord[:-1]):
       if sel_x <= min(ordered_x_coord[i], ordered_x_coord[i + 1]):
            if (iy <= sel_y <= ordered_y_coord[i+1]) or iy >= sel_y >= ordered_y_coord[i + 1]:
                    found_points.append((ordered_x_coord[i], ordered_y_coord[i], ordered_x_coord[i + 1], ordered_y_coord[i + 1]))
    return found_points


def get_index_to_remove(sel_y, found_points):
    # If we have any ranges that have a positive x-distance...
    # Then we need to examen those
    counter = 0
    index_to_remove = []
    # Get the points that have length larger than x...
    dist_x_points = [(ii, x) for ii, x in enumerate(found_points) if abs(x[0] - x[2]) > 0]
    for ii, range_x_point in dist_x_points:
        ix, iy, iix, iiy = range_x_point
        # Get the point that is NOT on the line for one edge point
        temp = [x for x in found_points if x[0] == ix and x != found_points[ii]]
        _, p_a, _, p_b = temp[0]
        ii_remove_0 = found_points.index(temp[0])
        temp = [x for x in [p_a, p_b] if x != sel_y]
        p0 = temp[0]
        # Get the OTHER point that is NOT on the line for one edge point
        temp = [x for x in found_points if x[0] == iix and x != found_points[ii]]
        # if len(temp) == 0:
        #     print('AAAAH')
        _, p_c, _, p_d = temp[0]
        ii_remove_1 = found_points.index(temp[0])
        temp = [x for x in [p_c, p_d] if x != sel_y]
        p1 = temp[0]
        # Compare. If they are UNEQUAL, then we have a proper break
        if ((p0 < sel_y) and (p1 > sel_y)) or ((p0 > sel_y) and (p1 < sel_y)):
            # NOW this counts as a break.. so
            counter += 1
        else:
            counter += 0
        # Since the x-range was the center index, we can remove the neighbours...
        index_to_remove.extend([ii_remove_0, ii, ii_remove_1])
    return index_to_remove, counter


pool_part2_tuple = [tuple(x) for x in pool_part2]
# Remove the last one because we already have that one..
pool_part2_tuple = pool_part2_tuple[:-1]
pool_x_coord, pool_y_coord = zip(*pool_part2)
sorted_pool_x_coord = [min_x] + sorted(set(pool_x_coord)) + [max_x]
n_x = len(sorted_pool_x_coord)
sorted_pool_y_coord = [min_y] + sorted(set(pool_y_coord)) + [max_y]
n_y = len(sorted_pool_y_coord)
i_x_grid = n_x // 2
i_y_grid = n_y // 2
do_break = False
valid_gridpoint_index = []
for i_x_grid in range(n_x-1):
    for i_y_grid in range(n_y-1):
        sel_x = sorted_pool_x_coord[i_x_grid]
        sel_y = sorted_pool_y_coord[i_y_grid]
        #
        sel_x1 = sorted_pool_x_coord[i_x_grid]
        sel_y1 = sorted_pool_y_coord[i_y_grid + 1]
        #
        sel_x2 = sorted_pool_x_coord[i_x_grid + 1]
        sel_y2 = sorted_pool_y_coord[i_y_grid]
        #
        dist_x = abs(sel_x2 - sel_x)
        dist_y = abs(sel_y1 - sel_y)
        if (sel_x, sel_y) in pool_part2_tuple:
            # Now it is in the path..
            if dist_x * dist_y == 1:
                # Skip it...
                pass
            else:
                # Lets check it
                # Now check if this point is...valid..?
                mid_x = sel_x + dist_x // 2
                mid_y = sel_y + dist_y // 2
                # print("midxmidy", mid_x, mid_y)
                found_points = get_other_coords(mid_x, mid_y, pool_x_coord, pool_y_coord)
                found_points = sorted(found_points)
                if len(found_points) > 0:
                    index_to_remove, counter = get_index_to_remove(mid_y, found_points)
                    # Mark which one to remove
                    for ii in index_to_remove:
                        found_points[ii] = None
                    # The remaining points are all single wall boundaries...
                    found_points = [x for x in found_points if x is not None]
                    counter += len(found_points)
                    if counter % 2 == 1:
                        valid_gridpoint_index.append((i_x_grid, i_y_grid))
        else:
            # Now check if this point is...valid..?
            mid_x = sel_x + dist_x // 2
            mid_y = sel_y + dist_y // 2
            # print("midxmidy", mid_x, mid_y, sel_x, dist_x, sel_y, dist_y)
            found_points = get_other_coords(mid_x, mid_y, pool_x_coord, pool_y_coord)
            found_points = sorted(found_points)
            if len(found_points) > 0:
                index_to_remove, counter = get_index_to_remove(mid_y, found_points)
                # Mark which one to remove
                for ii in index_to_remove:
                    found_points[ii] = None
                # The remaining points are all single wall boundaries...
                found_points = [x for x in found_points if x is not None]
                counter += len(found_points)
                if counter % 2 == 1:
                    valid_gridpoint_index.append((i_x_grid, i_y_grid))

    if do_break:
        break
#
# A = np.zeros(((max_x - min_x), (max_y - min_y)))
# for i_pool in pool_part2[:-1]:
#     ix, iy = i_pool
#     A[ix + abs(min_x), iy + abs(min_y)] += 5
#
# plt.imshow(A)
#
# # This is fucking insnae
# # Now lets check the value of each grid point...
# for i_x_grid, i_y_grid in valid_gridpoint_index:
#     ix = sorted_pool_x_coord[i_x_grid]
#     iy = sorted_pool_y_coord[i_y_grid]
#     A[ix + abs(min_x), iy + abs(min_y)] += 1
#
# plt.imshow(A)

total_surface = 0
for i_x_grid, i_y_grid in valid_gridpoint_index:
    sel_x = sorted_pool_x_coord[i_x_grid]
    sel_y = sorted_pool_y_coord[i_y_grid]
    # print(sel_x + abs(min_x), sel_y + abs(min_y))
    point_in_path = len([(x, y) for x, y in vertex_list if (sel_x in x) and (sel_y in y)])

    sel_y1 = sorted_pool_y_coord[i_y_grid + 1]
    sel_x2 = sorted_pool_x_coord[i_x_grid + 1]
    # print(sel_x + abs(min_x), sel_y1 + abs(min_y))
    # print(sel_x2 + abs(min_x), sel_y + abs(min_y))
    #
    dist_x = abs(sel_x2 - sel_x)
    dist_y = abs(sel_y1 - sel_y)
    surface = dist_x * dist_y
    temp_surface = 0
    # Okay what is ON the path needs to be improved...
    if point_in_path:
        if surface == 1:
            # Dont add... we do that later
            continue
        else:
            temp_surface = surface - 1
            # Do a fancy trick
            point_in_path_1 = len([(x, y) for x, y in vertex_list if (sel_x in x) and (sel_y1 in y)]) > 0
            point_in_path_0_1 = len([(x, y) for x, y in vertex_list if (sel_x in x) and (sel_y + 1 in y)]) > 0

            point_in_path_2 = len([(x, y) for x, y in vertex_list if (sel_x2 in x) and (sel_y in y)]) > 0
            point_in_path_0_2 = len([(x, y) for x, y in vertex_list if (sel_x + 1 in x) and (sel_y in y)]) > 0

            # If the x-coord is part of the path...
            if point_in_path_1:
                if point_in_path_0_1:
                    temp_surface -= dist_y - 1
                # else:
                #     temp_surface -= 1

            if point_in_path_2:
                # And there is a connection to it...
                if point_in_path_0_2:
                    temp_surface -= dist_x - 1
    else:
        temp_surface = surface

    print(temp_surface, end='\n\n')
    total_surface += temp_surface

# Now... the length of the path...
total_surface + wall_distance

# 1101771328793 too low....
# 129373230496292

