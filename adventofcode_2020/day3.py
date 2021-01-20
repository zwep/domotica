
with open("adventofcode_2020/day3_numbers.txt", "r") as f:
    A = f.readlines()

A_read = [x.strip() for x in A]

slope_down = 1
slope_right = 3
counter = 0
line_obj_list = []
line_index_list = []
for i_down, i_line in enumerate(A_read):
    sel_index = i_down * slope_right
    sel_index = sel_index % len(i_line)
    # print(i_down, sel_index, counter)
    line_obj = i_line[sel_index]

    line_index_list.append(sel_index)
    line_obj_list.append(line_obj)
    if line_obj == "#":
        counter += 1

print(counter)

# Alternative to one...
import re
with open("adventofcode_2020/day3_numbers.txt", "r") as f:
    A = f.read()

A = re.sub("\n", "", A)
print(list(A[0::34]))

line_index_list_alt = []
for i in np.arange(0, 323*31, 34):
    line_index_list_alt.append(i % 31)

for i, j in zip(line_index_list_alt, line_index_list):
    if i!=j:
        print(i,j)

for i, j, k, l in zip(line_index_list_alt, list(A[0::34]), line_index_list, line_obj_list):
    print(i,j, '\t', k, l)



# Part 2
with open("adventofcode_2020/day3_numbers.txt", "r") as f:
    A = f.readlines()

A_read = [x.strip() for x in A]


def get_trees(slope_down, slope_right, A, debug=False):
    counter = 0
    for i_down, i_line in enumerate(A[::slope_down]):
        sel_index = i_down * slope_right
        sel_index = sel_index % len(i_line)
        if debug:
            print(i_down, sel_index, counter)

        line_obj = i_line[sel_index]
        if line_obj == "#":
            counter += 1

    return counter

import numpy as np
res = []
for i_down, i_right in [(1, 1), (1, 3), (1,5), (1,7), (2,1)]:w
    n_trees = get_trees(i_down, i_right, A_read)
    res.append(n_trees)

print(res)
np.prod(res)