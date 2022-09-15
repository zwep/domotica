import numpy as np
import sys
"""

"""

test_case = "5483143223\n" \
     "2745854711\n" \
     "5264556173\n" \
     "6141336146\n" \
     "6357385478\n" \
     "4167524645\n" \
     "2176841721\n" \
     "6882881134\n" \
     "4846848554\n" \
     "5283751526"
#
# test_case = "11111\n" \
#             "19991\n" \
#             "19191\n" \
#             "19991\n" \
#             "11111"
#

puzzle_input = "8548335644\n" \
               "6576521782\n" \
               "1223677762\n" \
               "1284713113\n" \
               "6125654778\n" \
               "6435726842\n" \
               "5664175556\n" \
               "1445736556\n" \
               "2248473568\n" \
               "6451473526"

def indices_larger_than_nine(x, previous_indices=None):
    if previous_indices is None:
        previous_indices = np.ones(x.shape, dtype=bool)

    return (x > 9) * (previous_indices)


def update_matrix(A, A_ind):
    # print("\n\nStarting indices ", np.argwhere(A_ind))
    A_coord = np.argwhere(A_ind)
    # Do this for all indices...
    if len(A_coord):
        for sel_coord in A_coord:
            x_neighbour = sel_coord + np.array([[0, 1], [1, 0], [-1, 0], [0, -1], [1, 1], [-1, -1], [1, -1], [-1, 1]])
            inside_1 = np.all(x_neighbour < n_max, axis=1)
            inside_2 = np.all(0 <= x_neighbour, axis=1)
            inside_indices = inside_1 * inside_2
            # Add to these locations a 1...
            coord_x, coord_y = zip(*x_neighbour[inside_indices])
            A[coord_x, coord_y] += 1
            # print(sel_coord, "\nStatus", A)
        coord_x, coord_y = zip(*A_coord)
        A[coord_x, coord_y] = 0
    return A

# Get the number of total flashes after 100 steps
# During a step we
# - increase the energy level by 1
# -- Then we check which are larger than 9
# -- Each individual element then flashed to all its neighbours, raising energy by 1
# -- After a flash, its value is set to 0 and wont increase again

# A = np.array([np.array(list(x)) for x in test_case.split('\n')]).astype(int)
A = np.array([np.array(list(x)) for x in puzzle_input.split('\n')]).astype(int)

n_max, _ = A.shape
n_steps = 1000
s = 0
for istep in range(n_steps):
    A += 1
    A_ind = (A > 9)
    temp_value = A_ind.sum()
    # if temp_value == 100:
    if (A==0).sum() == 100:
        print(istep)
    s += temp_value
    A_coord_legacy = np.argwhere(A_ind)
    while any(A_ind.ravel()):
        A = update_matrix(A, A_ind)
        A_ind = (A > 9)
        temp_value = A_ind.sum()
        s += temp_value
        temp_A_coord = np.argwhere(A_ind)
        A_coord_legacy = np.concatenate([A_coord_legacy, temp_A_coord])
        coord_x, coord_y = zip(*A_coord_legacy)
        A[coord_x, coord_y] = 0
    if (A==0).sum() == 100:
        print(istep)

print(istep)
