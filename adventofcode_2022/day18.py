import os
import time
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def coord_to_set(y):
    return set([tuple(x) for x in y])


def coord_to_list(y):
    return list([list(x) for x in y])


def coord_to_tuple(y):
    return list([tuple(x) for x in y])


def coord_to_str(x):
    return ','.join([str(y) for y in x])


def coord_str_to_array(x):
    return np.array(list(map(int, x.split(','))))


def add_and_filter(ground_truth, displacement, axis):
    # Here we add a displacement to the points that we have
    # We keep those points that are not in the original set anymore
    # In that way we obtain a boundary
    delta = np.zeros(3, dtype=int)
    delta[axis] = displacement
    deviated = ground_truth + delta
    # Very cumbersome way to check if something is in there...
    # If the deviated coords are IN the ground truth, we DONT want them
    deviated = [x for x in deviated if not any((x == ground_truth).sum(axis=1) == 3)]
    return np.array(deviated)


def check_extreme_point(point_to_evaluate, ground_truth):
    # We also need to remove any 'outliers' from  the coordinates that we displaced with the previous function..
    #
    # We could've used the neighbour dict that we first somewhere created...?
    # But that also contains the z-coordinates...
    # Isnt that also necessary to consider?
    # Yes... yes it was.
    #
    # Here we check whether we have a point on the outside
    # This is done by checking if it the largest or lowest x-value in a specific row
    # Similarly for the largest/smallest y-value in a specific column
    filtered_points = []
    # We also need to rotate stuff in 45 degree to get specific other points..
    theta_x = np.deg2rad(45)
    rot_x_pos = np.array([[np.cos(theta_x), -np.sin(theta_x), 0],
                      [np.sin(theta_x), np.cos(theta_x), 0],
                      [0, 0, 1]])
    theta_x = np.deg2rad(-45)
    rot_x_neg = np.array([[np.cos(theta_x), -np.sin(theta_x), 0],
                          [np.sin(theta_x), np.cos(theta_x), 0],
                          [0, 0, 1]])

    for i_point in point_to_evaluate:
        x, y, z = i_point
        res = test_point(x, y, ground_truth)
        ground_truth_rot_pos = ((ground_truth - i_point) @ rot_x_pos) + i_point
        ground_truth_rot_neg = ((ground_truth - i_point) @ rot_x_neg) + i_point
        # Biggest hack in history. Just cast it to an int
        # WHAT CAN POSSIBLY GO WRONG
        # Okay things went wrong. We use ceil and floor now...
        res_rot_pos1 = test_point(x, y, np.ceil(ground_truth_rot_pos).astype(int))
        res_rot_pos2 = test_point(x, y, np.floor(ground_truth_rot_pos).astype(int))
        res_rot_neg1 = test_point(x, y, np.ceil(ground_truth_rot_neg).astype(int))
        res_rot_neg2 = test_point(x, y, np.floor(ground_truth_rot_neg).astype(int))
        #
        if res or res_rot_neg1 or res_rot_pos2 or res_rot_neg2 or res_rot_pos1:
            continue
        else:
            filtered_points.append(i_point)

    # # Print stuff
    # xx, yy = ground_truth[:, :2].T
    # fig, ax = plt.subplots()
    # ax.scatter(xx, yy)
    # ax.scatter(*ground_truth_rot_neg.astype(int).T[:2])
    # i_point = np.array([1, 11, 1])
    # ax.scatter(x, y)

    return np.array(filtered_points)


def test_point(x, y, ground_truth):
    x_coord = ground_truth[ground_truth[:, 1] == y, 0]
    y_coord = ground_truth[ground_truth[:, 0] == x, 1]
    x_bool = all(x > x_coord) or all(x < x_coord)
    y_bool = all(y > y_coord) or all(y < y_coord)
    return x_bool or y_bool


def find_lonely_points(x):
    # And remove them
    x_str = [coord_to_str(ix) for ix in x]
    filtered_stuff = []
    for ix in x:
        ix1 = coord_to_str(ix + np.array([0, 1, 0]))
        ix2 = coord_to_str(ix + np.array([0, -1, 0]))
        ix3 = coord_to_str(ix + np.array([1, 0, 0]))
        ix4 = coord_to_str(ix + np.array([-1, 0, 0]))
        if (ix1 not in x_str) and (ix2 not in x_str) and (ix3 not in x_str) and (ix4 not in x_str):
            print('derp', ix)
        else:
            filtered_stuff.append(ix)
    return filtered_stuff


"""
Read in the data
"""

dfile = os.path.join(DPATH, 'day18.txt')
with open(dfile, 'r') as f:
    puzzle_input = [list(map(int, x.strip().split(","))) for x in f.readlines()]

# Here we convert the data to different formats
array_of_coords = np.array([np.array(x) for x in puzzle_input])

# Here we can plot the number of coords
fig = plt.figure()
ax3d = fig.add_subplot(1, 1, 1, projection='3d')
ax3d.scatter(*array_of_coords.T)
ax3d.set_xlim(0, 10)


def get_inside_points(array_of_coords):
    _, _, min_z = np.min(array_of_coords, axis=0)
    _, _, max_z = np.max(array_of_coords, axis=0)

    inside_points = []
    for i_z in range(min_z, max_z+1):
        bool_z_loc = array_of_coords[:, 2] == i_z
        sel_array = array_of_coords[bool_z_loc]
        # Lets remove all the lonesome points..
        # sel_array = np.array(find_lonely_points(sel_array))
        if len(sel_array):
            for i_delta in [-1, 1]:
                for i_ax in [0, 1]:
                    temp = add_and_filter(sel_array, i_delta, i_ax)
                    temp = check_extreme_point(temp, ground_truth=sel_array)
                    if len(temp):
                        inside_points.extend([list(x) for x in temp])

    inside_points_str = [coord_to_str(x) for x in inside_points]
    inside_points_str = list(set(inside_points_str))
    inside_points_array = np.array([coord_str_to_array(x) for x in inside_points_str])
    return inside_points_str, inside_points_array

inside_points_str1, inside_points_array1 = get_inside_points(array_of_coords)
# Lets move the z to the x position
_, inside_points_array2 = get_inside_points(np.roll(array_of_coords, 1, axis=1))
inside_points_array2 = np.roll(inside_points_array2, -1, axis=1)
inside_points_str2 = [coord_to_str(x) for x in inside_points_array2]
# Now letz move z to the y position?
_, inside_points_array3 = get_inside_points(np.roll(array_of_coords, 2, axis=1))
inside_points_array3 = np.roll(inside_points_array3, -2, axis=1)
inside_points_str3 = [coord_to_str(x) for x in inside_points_array3]

len(inside_points_str1)
len(inside_points_str2)
len(set(inside_points_str1).intersection(set(inside_points_str2)).intersection(set(inside_points_str3)))
is_this_the_true_set = set(inside_points_str1).intersection(set(inside_points_str2)).intersection(set(inside_points_str3))
inside_points_str = list(is_this_the_true_set)
is_this_the_true_array = np.array([coord_str_to_array(x) for x in is_this_the_true_set])

#
# i_z = 19 heeft een fout
# i_z 16 ook
# Mijn idee werkt niet...
#
#
# # Plot everything...
# for i_z in range(min_z, max_z+1):
#     fig, ax = plt.subplots()
#     inside_i_z = inside_points_array[inside_points_array[:, 2] == i_z]
#     points_i_z = array_of_coords[array_of_coords[:, 2] == i_z]
#     inside_i_z[:, 2] = 20  # Set the size
#     points_i_z[:, 2] = 15  # Set the size
#     ax.scatter(*inside_i_z.T, zorder=999, facecolors='none', edgecolors='r')
#     ax.scatter(*points_i_z.T, 'k')
#     fig.suptitle(str(i_z))


# Some points are marked as inside but are not. Example:
# - When it is on the exterior but it has a floating point around it, not attached to the big circle. Making it not the biggest
# or the smallest x/y value...
"""
Find the neighbours...
"""

cube_dict = {}
list_of_coords = [coord_to_str(x) for x in puzzle_input]
set_of_coords = set(list_of_coords)
# set_of_coords = set(list_of_coords + inside_points_str)
#for i_coord_str in list_of_coords + inside_points_str:
for i_coord_str in inside_points_str:
    # Give everyone 6 sides
    cube_dict.setdefault(i_coord_str, 6)
    set_coord_str = set(i_coord_str)
    array_coord = coord_str_to_array(i_coord_str)
    # Remove the coord we are looking at
    set_remaining_coords = set_of_coords.difference(set_coord_str)
    # Create an array of the remaining coords
    array_remaining_coords = np.array([x.split(',') for x in set_remaining_coords], int)
    # Calculate the distance of the current coord to the others...
    difference_coords = np.abs(array_coord - array_remaining_coords).sum(axis=1)
    if any(difference_coords == 1):
        location_sides = difference_coords == 1
        n_sides = sum(location_sides)
        cube_dict[i_coord_str] = cube_dict[i_coord_str] - n_sides

sum([v for k, v in cube_dict.items() if k in list_of_coords])
# New answer...
# 4192 comes from the first part
4192 - sum([6 - v for k, v in cube_dict.items() if k in inside_points_str])


# 2508 too low
# 2533 wrong..
# 2537 wrong.. as well.. this was a quick guess
# 2625 too high
# 2738 (new since jan 2023)
# 3328 too high

