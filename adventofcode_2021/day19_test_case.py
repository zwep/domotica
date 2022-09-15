
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


with open('/home/bugger/Documents/data/aoc/2021/input_day_19_test.txt') as f:
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

scanner_location_dict = {}
scanner_rotation_dict = {}
beacon_location_dict = {}
scanner_name_list = list(full_dict.keys())
n_scanners = len(scanner_name_list)
connectivity_matrix = np.zeros((n_scanners, n_scanners))
for i_name in range(n_scanners):
    for j_name in range(n_scanners):
        find = False
        scanner_name_0 = scanner_name_list[i_name]
        scanner_name_1 = scanner_name_list[j_name]
        dict_result_name = f"{scanner_name_0}->{scanner_name_1}"
        dict_result_name2 = f"{scanner_name_1}->{scanner_name_0}"
        print(dict_result_name)
        scanner_location_dict.setdefault(dict_result_name, np.array([0, 0, 0]))
        scanner_rotation_dict.setdefault(dict_result_name, np.array([0, 0, 0]))
        beacon_location_dict.setdefault(dict_result_name, [])
        # Get stuff for number 0
        beacon_coords_0 = full_dict[scanner_name_0]
        dist_matrix_0 = get_dist_mat(beacon_coords_0)
        n_beacons_0 = dist_matrix_0.shape[0]
        # Get stuff for number 1
        beacon_coords_1 = full_dict[scanner_name_1]
        dist_matrix_1 = get_dist_mat(beacon_coords_1)
        n_beacons_1 = dist_matrix_1.shape[0]
        for i_beacon in range(n_beacons_0):
            for j_beacon in range(n_beacons_1):
                dist_matrix_relative = dist_matrix_0[i_beacon] - dist_matrix_1[j_beacon][None].T
                zero_matrix = np.argwhere(np.isclose(dist_matrix_relative, 0))
                n_row = zero_matrix.shape[0]
                if n_row >= 12:
                    overlap_beacon_0 = beacon_coords_0[zero_matrix[:, 1]]
                    overlap_beacon_1 = beacon_coords_1[zero_matrix[:, 0]]
                    # Lets see if we can find a rotation/translation
                    abs_location, rotation_1_to_0 = get_abs_coords_and_rotation(overlap_beacon_0, overlap_beacon_1)
                    print(abs_location, rotation_1_to_0)
                    scanner_location_dict[dict_result_name] = np.array(abs_location)
                    scanner_rotation_dict[dict_result_name2] = np.array(rotation_1_to_0)
                    beacon_location_dict[dict_result_name] = [overlap_beacon_0, overlap_beacon_1]
                    find = True

                    if i_name != j_name:
                        connectivity_matrix[i_name, j_name] = 1
                    break
            if find:
                break

plt.imshow(connectivity_matrix)
rot_mat_1_0 = get_3d_rot(*scanner_rotation_dict['scanner 1->scanner 0']).astype(int)
rot_mat_3_1 = get_3d_rot(*scanner_rotation_dict['scanner 3->scanner 1']).astype(int)
rot_mat_4_1 = get_3d_rot(*scanner_rotation_dict['scanner 4->scanner 1']).astype(int)
rot_mat_2_4 = get_3d_rot(*scanner_rotation_dict['scanner 2->scanner 4']).astype(int)
scanner_location_dict['scanner 0->scanner 3'] = scanner_location_dict['scanner 1->scanner 3'] @ rot_mat_1_0 + scanner_location_dict['scanner 0->scanner 1']
loc_3 = np.array(full_dict['scanner 3'])
loc_3_translated = loc_3 @ rot_mat_3_1 @ rot_mat_1_0 + scanner_location_dict['scanner 0->scanner 3']

scanner_location_dict['scanner 0->scanner 4'] = scanner_location_dict['scanner 1->scanner 4'] @ rot_mat_1_0 + scanner_location_dict['scanner 0->scanner 1']
scanner_location_dict['scanner 0->scanner 2'] = scanner_location_dict['scanner 4->scanner 2'] @ rot_mat_4_1 @ rot_mat_1_0 + scanner_location_dict['scanner 0->scanner 4']

loc_0 = np.array(full_dict['scanner 0'])
loc_1 = np.array(full_dict['scanner 1'])
loc_2 = np.array(full_dict['scanner 2'])

loc_4 = np.array(full_dict['scanner 4'])

loc_1_translated = loc_1 @ rot_mat_1_0 + scanner_location_dict['scanner 0->scanner 1']

loc_4_translated = loc_4 @ rot_mat_4_1  @ rot_mat_1_0 + scanner_location_dict['scanner 0->scanner 4']
loc_2_translated = loc_2 @ rot_mat_2_4 @ rot_mat_4_1  @ rot_mat_1_0 + scanner_location_dict['scanner 0->scanner 2']
stacked_locations = np.concatenate([loc_0, loc_1_translated, loc_2_translated, loc_3_translated, loc_4_translated], axis=0)
stacked_locations.shape
own_output_list = np.unique(stacked_locations, axis=0)

with open('/home/bugger/Documents/data/aoc/2021/output_day_19_test.txt') as f:
    output_list = f.readlines()

output_list = np.array([list(map(int, x.strip().split(","))) for x in output_list])

own_output_list == output_list

