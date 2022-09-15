
# Oke en dan nu verder coden...

import re
import matplotlib.pyplot as plt
import numpy as np
import itertools


def rot_x(degrees):
    # X-rotation matrix
    theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    rot_mat = np.array([[1, 0, 0], [0, c, -s],  [0, s, c]])
    return rot_mat


def rot_y(degrees):
    # Y-rotation matrix
    theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    rot_mat = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return rot_mat


def rot_z(degrees):
    # Z-rotation matrix
    theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    rot_mat = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    return rot_mat


def get_3d_rot(x_angle, y_angle, z_angle):
    return rot_x(x_angle) @ rot_y(y_angle) @ rot_z(z_angle)


def get_dist_mat(scanner_array):
    # Incomming shape is (npoints, ndim)
    # This truely counters the orientation problem. Which is nice
    n_points, n_dim = scanner_array.shape
    dist_matrix = np.zeros((n_points, n_points))
    for ii in range(n_dim):
        dist_matrix += ((scanner_array[:, ii:ii + 1] - scanner_array[:, ii:ii + 1].T)) ** 2
    dist_matrix = np.sqrt(dist_matrix)
    return dist_matrix


def get_manhattan_mat(scanner_array):
    # Incomming shape is (npoints, ndim)
    # This truely counters the orientation problem. Which is nice
    n_points, n_dim = scanner_array.shape
    dist_matrix = np.zeros((n_points, n_points))
    for ii in range(n_dim):
        dist_matrix += np.abs(((scanner_array[:, ii:ii + 1] - scanner_array[:, ii:ii + 1].T)))
    return dist_matrix


def get_abs_coords_and_rotation(coords_0, coords_1):
    possible_angles = np.arange(0, 360, 90)
    # Dit zijn te veel hoeken... ik heb er 64 maar ik hoef er maar 24...
    all_possible_angles = itertools.product(possible_angles, possible_angles, possible_angles)
    final_location = None
    final_rotation = None
    for x_angle, y_angle, z_angle in all_possible_angles:
        rot_mat = rot_x(x_angle) @ rot_y(y_angle) @ rot_z(z_angle)
        result_mat = coords_0 - coords_1 @ rot_mat.astype(int)
        if all(np.isclose(np.diff(result_mat, axis=0).sum(axis=0), 0)):
            final_location = result_mat[0]
            final_rotation = [x_angle, y_angle, z_angle]
            # print(final_location, final_rotation)
            break
    return final_location, final_rotation


with open('/home/bugger/Documents/data/aoc/2021/input_day_19.txt') as f:
    input_list = f.readlines()


full_dict = {}
scanner_name = None
temp_dict = {}
for i_line in input_list:
    if i_line.startswith('---'):
        # Only add it the full_dict if we have any processed lines
        if len(temp_dict):
            # Conert to a numpy array to make processing easier
            for k, v in temp_dict.items():
                temp_dict[k] = np.array(v)
            full_dict.update(temp_dict)
        # Start a new scanner...
        temp_dict = {}
        scanner_name = re.sub("---", "", i_line).strip()
        temp_dict.setdefault(scanner_name, [])
    elif len(i_line) > 1:
        # Keep adding lines in x,y,z coordinates (relative)
        x, y, z = i_line.strip().split(",")
        temp_dict[scanner_name].append([int(x), int(y), int(z)])

"""
Different point of view now..

We will create a collection of rotated beacons.. lets see how that goes..

--> This one worked
"""

scanner_location_dict = {}
scanner_name_list = list(full_dict.keys())
n_scanners = len(scanner_name_list)
connectivity_matrix = np.zeros((n_scanners, n_scanners))
unvisited_scanners = list(range(n_scanners))[::-1]
validated_beacons = full_dict['scanner 0']
while unvisited_scanners:
    print('Unvisited scanners ', unvisited_scanners)
    # i_name = unvisited_scanners.pop()
    # print('Popped query', i_name)
    for j_name in unvisited_scanners:
        print(f'Checking scanner {j_name}', end='\r')
        find = False
        scanner_name_1 = scanner_name_list[j_name]
        # Get stuff for validated
        dist_matrix_validated = get_dist_mat(validated_beacons)
        n_beacons_validated = dist_matrix_validated.shape[0]
        # Get stuff for number 1
        beacon_coords_1 = full_dict[scanner_name_1]
        dist_matrix_1 = get_dist_mat(beacon_coords_1)
        n_beacons_1 = dist_matrix_1.shape[0]
        for i_beacon in range(n_beacons_validated):
            for j_beacon in range(n_beacons_1):
                dist_matrix_relative = dist_matrix_validated[i_beacon] - dist_matrix_1[j_beacon][None].T
                zero_matrix = np.argwhere(np.isclose(dist_matrix_relative, 0))
                n_row = zero_matrix.shape[0]
                if n_row >= 12:
                    # validated_beacons
                    overlap_beacon_validated = validated_beacons[zero_matrix[:, 1]]
                    overlap_beacon_1 = beacon_coords_1[zero_matrix[:, 0]]
                    # Lets see if we can find a rotation/translation
                    abs_location_val_to_1, rotation_1_to_val = get_abs_coords_and_rotation(overlap_beacon_validated, overlap_beacon_1)
                    scanner_location_dict[f'scanner {j_name}'] = abs_location_val_to_1
                    rotated_beacons_1 = beacon_coords_1 @ get_3d_rot(*rotation_1_to_val).astype(int) + abs_location_val_to_1
                    validated_beacons = np.concatenate([validated_beacons, rotated_beacons_1])
                    validated_beacons = np.unique(validated_beacons, axis=0)
                    find = True
                    break
            if find:
                print('\t Seen scanner ', j_name)
                # query_scanners.append(j_name)
                unvisited_scanners.pop(unvisited_scanners.index(j_name))
                print('\t New unvisited scanners ', unvisited_scanners)
                break

print("Number of beacons ", validated_beacons.shape[0])

abs_loc_mat = np.array(list(scanner_location_dict.values()))
np.max(get_manhattan_mat(abs_loc_mat))