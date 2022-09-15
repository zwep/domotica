
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
visited_scanners = []
unvisited_scanners = list(range(n_scanners))[::-1]
query_scanners = [0]
while query_scanners:
    print('Querry list ', query_scanners)
    i_name = query_scanners.pop()
    print('Popped query', i_name)
    visited_scanners.append(i_name)
    unvisited_scanners = list(set(unvisited_scanners).difference(set(visited_scanners)))
    for j_name in unvisited_scanners:
        print(f'Checking scanner {j_name}', end='\r')
        find = False
        scanner_name_0 = scanner_name_list[i_name]
        scanner_name_1 = scanner_name_list[j_name]
        dict_result_name_0_to_1 = f"{scanner_name_0}->{scanner_name_1}"
        dict_result_name_1_to_0 = f"{scanner_name_1}->{scanner_name_0}"
        # print(dict_result_name)
        scanner_location_dict.setdefault(dict_result_name_0_to_1, [])
        scanner_location_dict.setdefault(dict_result_name_1_to_0, [])
        #  Also the other way around..? I think I need that
        scanner_rotation_dict.setdefault(dict_result_name_0_to_1, [])
        scanner_rotation_dict.setdefault(dict_result_name_1_to_0, [])
        beacon_location_dict.setdefault(dict_result_name_0_to_1, [])
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
                    abs_location_0_to_1, rotation_1_to_0 = get_abs_coords_and_rotation(overlap_beacon_0, overlap_beacon_1)
                    abs_location_1_to_0, rotation_0_to_1 = get_abs_coords_and_rotation(overlap_beacon_1, overlap_beacon_0)
                    # print(abs_location, rotation_1_to_0)
                    scanner_location_dict[dict_result_name_0_to_1] = np.array(abs_location_0_to_1)
                    scanner_location_dict[dict_result_name_1_to_0] = np.array(abs_location_1_to_0)
                    scanner_rotation_dict[dict_result_name_1_to_0] = np.array(rotation_1_to_0)
                    scanner_rotation_dict[dict_result_name_0_to_1] = np.array(rotation_0_to_1)
                    beacon_location_dict[dict_result_name_0_to_1] = [overlap_beacon_0, overlap_beacon_1]
                    beacon_location_dict[dict_result_name_1_to_0] = [overlap_beacon_1, overlap_beacon_0]
                    find = True
                    # if i_name != j_name:
                    connectivity_matrix[i_name, j_name] = 1
                    break
            if find:
                print('\t Adding scanner ', j_name)
                query_scanners.append(j_name)
                print('\t New Query ', query_scanners)
                break

# plt.imshow(connectivity_matrix)
import networkx as nx
DG = nx.from_numpy_matrix(connectivity_matrix)
# Add direction...
index_scanner_order = np.argsort([len(list(nx.all_shortest_paths(DG, 0, i_scanner))[0]) for i_scanner in range(1, n_scanners)])+1


all_beacons = []
i_scanner = 2
# Maybe this solves stuff..?
scanner_location_dict[f'scanner 0->scanner 0'] = np.array([0,0,0])
for i_scanner in index_scanner_order:
    path_to_scanner = list(nx.all_shortest_paths(DG, 0, i_scanner))[0]
    print(i_scanner, path_to_scanner)
    # n_sub_groups = int(np.ceil(len(path_to_scanner) / 2))
    # temp = [path_to_scanner[i:i + 2] for i in range(n_sub_groups)]
    source_loc = path_to_scanner[-2]
    tgt_loc = path_to_scanner[-1]
    rot_mat_source_tgt = get_3d_rot(*scanner_rotation_dict[f'scanner {tgt_loc}->scanner {source_loc}']).astype(int)
    rotation_order = path_to_scanner[::-1][1:]
    n_sub_groups = int(np.ceil(len(rotation_order)/2))
    rotation_matrix_index = [rotation_order[i:i+2] for i in range(n_sub_groups)]
    rot_mat = np.eye(3)
    if len(rotation_matrix_index[0]) > 1:
        for i_rot_index in rotation_matrix_index:
            prev, next = i_rot_index
            rot_mat_prev_next = get_3d_rot(*scanner_rotation_dict[f'scanner {prev}->scanner {next}']).astype(int)
            rot_mat = rot_mat @ rot_mat_prev_next
    scanner_location_dict[f'scanner 0->scanner {i_scanner}'] = scanner_location_dict[f'scanner {source_loc}->scanner {tgt_loc}'] @ rot_mat + scanner_location_dict[f'scanner 0->scanner {source_loc}']
    loc_beacons = np.array(full_dict[f'scanner {i_scanner}'])
    loc_beacons_translated = loc_beacons @ rot_mat_source_tgt @ rot_mat + scanner_location_dict[f'scanner 0->scanner {i_scanner}']
    # / Debug - focus only on the 12 overlapping beacons to validate the rotation
    # loc_source, loc_i = np.array(beacon_location_dict[f'scanner {source_loc}->scanner {i_scanner}'])
    # # abs_loc, rot_loc = get_abs_coords_and_rotation(loc_source, loc_i)
    # # Validate the rotation matrix..
    # # loc_source - (loc_i @ get_3d_rot(*rot_loc).astype(int) + abs_loc)
    # # This one below rotates towards 0
    # loc_i_translated = (loc_i @ rot_mat_source_tgt @ rot_mat + scanner_location_dict[f'scanner 0->scanner {i_scanner}'])
    # # This one below rotates towards the source
    # # loc_i_translated = (loc_i @ rot_mat_source_tgt + scanner_location_dict[f'scanner {source_loc}->scanner {tgt_loc}'])
    # # Below we also rotate the source locations towards scanner 0 and then check the overlap with the target locations rotated to scanner 0
    # first = np.concatenate([loc_source @ rot_mat + scanner_location_dict[f'scanner 0->scanner {source_loc}'], loc_i_translated])
    # # first = np.concatenate([loc_source, loc_i_translated])
    # second = np.unique(first, axis=0)
    # print(i_scanner, ' -> ', source_loc)
    # print(first.shape, second.shape)
    all_beacons.append(loc_beacons_translated)


all_beacons = np.concatenate(all_beacons)
stacked_locations = np.concatenate([all_beacons, full_dict[f'scanner 0']])
stacked_locations.shape
own_output_list = np.unique(stacked_locations, axis=0)
own_output_list.shape
