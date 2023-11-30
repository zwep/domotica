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


def calculate_cube_sides(list_of_str_coords):
    """
    This is the main workhorse of problem part 1.
    By going over a list of coords, we check the distance of a coord to the rest
    and then do some funky calculations where we substract the number of neighbors from the starting value of 6
    It worked.
    :param list_of_str_coords:
    :return:
    """
    cube_dict = {}
    set_of_coords = set(list_of_str_coords)
    for i_coord_str in list_of_str_coords:
        # Give everyone 6 sides, and then
        cube_dict.setdefault(i_coord_str, 6)
        set_coord_str = set(i_coord_str)
        array_coord = coord_str_to_array(i_coord_str)
        # Remove the coord we are looking at
        set_remaining_coords = set_of_coords.difference(set_coord_str)
        # Create an array of the remaining coords
        array_remaining_coords = np.array([coord_str_to_array(x) for x in set_remaining_coords])
        # Calculate the distance of the current coord to the others...
        difference_coords = np.abs(array_coord - array_remaining_coords).sum(axis=1)
        if any(difference_coords == 1):
            location_sides = difference_coords == 1
            n_sides = sum(location_sides)
            cube_dict[i_coord_str] = cube_dict[i_coord_str] - n_sides
    return cube_dict


def calculate_cube_sides_v2(array_of_coords):
    """
    Version 2...
    """
    total_sides = 0
    n_coords = len(array_of_coords)
    for i in range(n_coords):
        next_coord = array_of_coords[i]
        difference_coords = np.abs(next_coord - array_of_coords).sum(axis=1)
        if any(difference_coords == 1):
            location_sides = difference_coords == 1
            n_sides = sum(location_sides)
            total_sides += n_sides
    return total_sides


def calculate_cube_sides_part2(array_of_coords, array_of_droplet_coords):
    """
    Part 2... get the number of coinciding sides
    For each boundary coord... calculate the distnace to the droplet
    If we have distances of 1, we count that
    """
    total_sides = 0
    n_coords = len(array_of_coords)
    for i in range(n_coords):
        next_coord = array_of_coords[i]
        difference_coords = np.abs(next_coord - array_of_droplet_coords).sum(axis=1)
        if any(difference_coords == 1):
            location_sides = difference_coords == 1
            n_sides = sum(location_sides)
            total_sides += n_sides
    return total_sides


def add_and_filter(ground_truth, displacement, axis):
    """

    :param ground_truth: array of coords
    :param displacement: integer either -1 or +1
    :param axis: integer equal to 0, 1, or 2
    :return:
    """
    # Here we add a displacement to the points that we have
    # We keep those points that are not in the original set anymore
    # In that way we obtain a boundary of some sorts
    # We do this over multiple axis to get a 3D boundary
    delta = np.zeros(3, dtype=int)
    delta[axis] = displacement
    deviated = ground_truth + delta
    # Very cumbersome way to check if something is in there...
    # If the deviated coords are IN the ground truth, we DONT want them
    deviated = [x for x in deviated if not any((x == ground_truth).sum(axis=1) == 3)]
    return np.array(deviated)


def visualize_points(array_of_coords, point_size=15, ax_dict=None, color='k'):
    if ax_dict is None:
        ax_dict = {}
        for i_z in range(MIN_Z-1, MAX_Z + 1):
            fig, ax = plt.subplots()
            ax_dict[i_z] = ax
    else:
        ax_dict = ax_dict

    for i_z in range(MIN_Z-1, MAX_Z + 1):
        points_i_z = array_of_coords[array_of_coords[:, 2] == i_z]
        points_i_z[:, 2] = point_size  # Set the size in the last axis..
        if i_z in ax_dict.keys():
            ax_dict[i_z].scatter(*points_i_z.T, color=color)
            ax_dict[i_z].set_xlim(MIN_X, MAX_X)
            ax_dict[i_z].set_ylim(MIN_Y, MAX_Y)
    return ax_dict

"""
There are two parts:

First part answer is 4192
"""

dfile = os.path.join(DPATH, 'day18.txt')
with open(dfile, 'r') as f:
    puzzle_input = [list(map(int, x.strip().split(","))) for x in f.readlines()]

# Here we convert the data to different formats
array_of_coords = np.array([np.array(x) for x in puzzle_input])
list_of_coords = [np.array(x) for x in puzzle_input]
MIN_X, MIN_Y, MIN_Z = np.min(array_of_coords, axis=0)
MAX_X, MAX_Y, MAX_Z = np.max(array_of_coords, axis=0)
list_of_str_coords = [coord_to_str(x) for x in puzzle_input]
n_coords = len(array_of_coords)
# Example of coords:
n_display = 10
sel_coords = np.random.randint(0, n_coords, n_display)
print("Example of the coordinates: ")
for i_coord in array_of_coords[sel_coords]:
    print(coord_to_str(i_coord))

# Here we can plot the number of coords
fig = plt.figure()
ax3d = fig.add_subplot(1, 1, 1, projection='3d')
ax3d.scatter(*array_of_coords.T)
fig.suptitle('Visualization of coords')

# Get the answer to part 1
# import time
# t0 = time.time()
# cube_side_dict = calculate_cube_sides(list_of_str_coords)
# print(time.time() - t0)
# total_surface_value_droplets = sum([v for k, v in cube_side_dict.items() if k in list_of_str_coords])
#
# copy_list_of_coords = np.copy(list_of_coords)
# t0 = time.time()
# res = calculate_cube_sides_v2(copy_list_of_coords)
# print(time.time() - t0)
# total_surface_value_droplets = len(copy_list_of_coords) * 6 - res

# Now we want to find the inside droplet, calculate their surface area and substract this from the previous answer
# So... we want to look INSIDE the droplet (since all the coords form some sort of circle)
# And get all those points, and calculate the surface of that again.
# This means I could re-use my previous method.
boundary_coords = []
for i_displacement in [-1, 1]:
    for i_axis in [0, 1, 2]:
        deviated_coords = add_and_filter(array_of_coords, displacement=i_displacement, axis=i_axis)
        boundary_coords.append(deviated_coords)

boundary_coords = np.concatenate(boundary_coords, axis=0)
boundary_coords_set = set([coord_to_str(x) for x in boundary_coords])
boundary_coords_array = np.array([coord_str_to_array(x) for x in boundary_coords_set])

# Now visualize the boundary coords...
# ax_dict = visualize_points(array_of_coords)
# ax_dict = visualize_points(boundary_coords_array, point_size=5, ax_dict=ax_dict, color='r')

# Now calculate the surface of these boundary coords with the droplet
# If we dont filter anything, we get the same result as the previous part...
# res_boundary = calculate_cube_sides_part2(boundary_coords_array, array_of_coords)

# Get the neighbours
def get_neighbours(i_point, point_cloud):
    neighbours = []
    for i_ax in range(3):
        for i_disp in [-1, 1]:
            disp_vector = np.zeros(3)
            disp_vector[i_ax] = i_disp
            new_point = i_point + disp_vector
            check_inside = any([all(x == new_point) for x in point_cloud])
            if check_inside:
                index_point = np.argwhere(np.abs(point_cloud - new_point).sum(axis=1) == 0).ravel()[0]
                neighbours.append(new_point)
    return neighbours

n_boundary = len(boundary_coords_array)
point_cloud_set = boundary_coords_set.copy()

sets_of_neighbours = []
remaining_set = []
while len(point_cloud_set):
    # Remove the first/last point, and go find its neighbours
    next_point_str = point_cloud_set.pop()
    print(next_point_str, len(point_cloud_set))
    neighbour_set = set()
    neighbour_set.add(next_point_str)
    # Initialize the first point...
    temp_neighbour_list = [next_point_str]
    while len(temp_neighbour_list):
        print('\t', len(neighbour_set))
        point_cloud = np.array([coord_str_to_array(x) for x in point_cloud_set])
        temp_point = temp_neighbour_list.pop()
        next_point = coord_str_to_array(temp_point)
        point_neighbours = get_neighbours(next_point, point_cloud=point_cloud)
        temp_result = [coord_to_str(x.astype(int)) for x in point_neighbours]
        # Remove the neighbours, we dont want to find these anymore..
        [point_cloud_set.remove(x) for x in temp_result]
        [neighbour_set.add(x) for x in temp_result]
        # Add neihbours to this list...
        temp_neighbour_list.extend(temp_result)
        remaining_set.append(len(point_cloud_set))
    # Store the found set of negihbours
    print("Starting over", len(point_cloud_set))
    sets_of_neighbours.append(neighbour_set)



# Nu heb ik alles wat buren is...
# Dus het probleem is nu gereduceerd naar het checken van deze 225 groepen.
# Wanneer is iets buiten..?

large_set_of_points = [x for x in sets_of_neighbours if len(x) > 100]
n_large = len(large_set_of_points)
color_list = plt.cm.get_cmap('hsv', len(sets_of_neighbours)+2)
ax_dict = visualize_points(array_of_coords)
for ii, i_set in enumerate(sets_of_neighbours[0:1]):
    temp = np.array([coord_str_to_array(x) for x in i_set])
    visualize_points(temp, point_size=5, ax_dict=ax_dict, color=color_list(ii))

# Check if a point is inside something... in all directions
status_groups = []
i_group = 0
for i_group in range(len(sets_of_neighbours)):
    sel_point = list(sets_of_neighbours[i_group])[0]
    sel_point_array = coord_str_to_array(sel_point)
    status = []
    for i_ax in [0, 1, 2]:
        print('Axes ', i_ax)
        for i_direction in [-1, 1]:
            print('Direction ', i_direction)
            found_point = False
            n_points = 1
            # Max points/directions to check is 20..
            while found_point is False and n_points < 20:
                disp_array = np.zeros(3)
                disp_array[i_ax] = i_direction * n_points
                temp_coord = sel_point_array + disp_array
                check_inside = any([all(x == temp_coord) for x in array_of_coords])
                if check_inside:
                    found_point = True
                    print('\t\t Found a point ', n_points)
                else:
                    n_points += 1
            status.append(found_point)
    status_groups.append(status)

inside_group_ind = np.argwhere(np.sum(status_groups, axis=1) == 6)
inside_group_ind = inside_group_ind.ravel()
ax_dict = visualize_points(array_of_coords)
for ii, i_set in enumerate(sets_of_neighbours):
    if ii in inside_group_ind:
        temp = np.array([coord_str_to_array(x) for x in i_set])
        visualize_points(temp, point_size=5, ax_dict=ax_dict, color=color_list(ii))

sel_boundary_coords_array = []
for ii, i_set in enumerate(sets_of_neighbours):
    if ii in inside_group_ind:
        sel_boundary_coords_array.extend([coord_str_to_array(x) for x in list(i_set)])

sel_boundary_coords_array = np.array(sel_boundary_coords_array)
res_boundary = calculate_cube_sides_part2(sel_boundary_coords_array, array_of_coords)
4192 - res_boundary

"""
Previous submissions to part 2:

2508 too low
2533 wrong..
2537 wrong.. as well.. this was a quick guess
2625 too high
2738 (new since jan 2023, but wrong)
3328 too high


"""
