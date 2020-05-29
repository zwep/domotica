
import matplotlib.pyplot as plt
import numpy as np
import subprocess
from api_secrets import day_3_input


# From commands to points in space...
def command_to_point(line_input):
    p0 = [0, 0]
    list_point = [p0]
    for i_obj in line_input:
        prev_point = list_point[-1]
        new_point = np.copy(prev_point)
        command = i_obj[0]
        step = int(i_obj[1:])
        if command == "R":
            new_point[0] = int(prev_point[0]) + step
        elif command == "L":
            new_point[0] = int(prev_point[0]) - step
        elif command == "U":
            new_point[1] = int(prev_point[1]) + step
        elif command == "D":
            new_point[1] = int(prev_point[1]) - step
        else:
            pass

        list_point.append(new_point)
    return list_point

"""
day 3a
"""

output = subprocess.check_output(['bash','-c', day_3_input])
input_args = [x.split(',') for x in output.decode().split('\n')]

line_0 = input_args[0]
line_1 = input_args[1]


point_0 = command_to_point(line_0)
point_1 = command_to_point(line_1)
plt.figure()
plt.scatter([x[0] for x in point_0], [x[1] for x in point_0])
plt.scatter([x[0] for x in point_0], [x[1] for x in point_1])

plt.figure()
plt.plot(point_0, 'r')
plt.plot(point_1, 'b')

line_0_x = [x[0] for x in point_0]
line_0_y = [x[1] for x in point_0]
line_1_x = [x[0] for x in point_1]
line_1_y = [x[1] for x in point_1]

plt.figure()
n_total_segments = len(line_0_x)
n_total_segments_inner = len(line_1_x)
result_scatter = []
result_segment = []

for i_segm in range(0, n_total_segments-1):
    X01 = line_0_x[i_segm]
    X02 = line_0_x[i_segm+1]
    Y01 = line_0_y[i_segm]
    Y02 = line_0_y[i_segm + 1]
    plt.plot([X01, X02], [Y01, Y02], 'r')

    for i_segm_inner in range(0, n_total_segments_inner-1):
        X11 = line_1_x[i_segm_inner]
        X12 = line_1_x[i_segm_inner + 1]
        Y11 = line_1_y[i_segm_inner]
        Y12 = line_1_y[i_segm_inner + 1]
        if i_segm == 0:
            plt.plot([X11, X12], [Y11, Y12], 'b')

        intersect_x = [max(min(X01, X02), min(X11, X12)), min(max(X01, X02), max(X11, X12))]
        intersect_y = [max(min(Y01, Y02), min(Y11, Y12)), min(max(Y01, Y02), max(Y11, Y12))]
        if intersect_x[0] <= intersect_x[1]:
            if intersect_y[0] <= intersect_y[1]:
                result_scatter.append((intersect_x[0], intersect_y[0]))
                result_segment.append((i_segm, i_segm_inner))

plt.scatter([x[0] for x in result_scatter], [x[1] for x in result_scatter], marker='x')

reference_point = result_scatter[0]
np.min([abs(reference_point[1] - x[1]) + abs(reference_point[0] - x[0]) for x in result_scatter][1:])

"""
Day3b
"""
main_length_0 = 0
main_length_1 = 0
total_length = []
for i in range(len(result_segment)):

    segment_line_0 = result_segment[i][0]  # Segment of line 0
    segment_line_1 = result_segment[i][1]  # Segment of line 1

    main_length_0 = int(sum([int(x[1:]) for x in line_0][:segment_line_0]))
    main_length_1 = int(sum([int(x[1:]) for x in line_1][:segment_line_1]))

    delta_0 = abs(line_0_y[segment_line_0] - result_scatter[i][1]) + abs(line_0_x[segment_line_0] - result_scatter[i][0])
    delta_1 = abs(line_1_y[segment_line_1] - result_scatter[i][1]) + abs(line_1_x[segment_line_1] - result_scatter[i][0])

    total_0 = main_length_0 + delta_0
    total_1 = main_length_1 + delta_1
    total_length.append(total_1 + total_0)

min(total_length[1:])