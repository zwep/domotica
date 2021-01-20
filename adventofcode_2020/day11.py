
def change_state(A):
    n_rows = len(A)
    n_cols = len(A[0])
    new_A = [['.'] * n_cols for _ in range(n_rows)]

    for i in range(n_rows):
        for j in range(n_cols):
            sel_pos = A[i][j]
            if sel_pos == ".":
                new_A[i][j] = "."
            else:
                neighhbour_status = []
                for ii in [-1, 0, 1]:
                    for jj in [-1, 0, 1]:
                        new_i = i + ii
                        new_j = j + jj
                        if new_i == -1 or new_i >= n_rows:
                            continue
                        if new_j == -1 or new_j >= n_cols:
                            continue
                        if ii == 0 and jj == 0:
                            continue
                        # index_to_go[new_i][new_j] += 1
                        neighbour_pos = A[new_i][new_j]
                        neighhbour_status.append(neighbour_pos)
                neighhbour_status = [x for x in neighhbour_status if x != '.']

                if sel_pos == 'L' and not any([x == '#' for x in neighhbour_status]):
                    new_A[i][j] = "#"
                elif sel_pos == '#' and sum([x == '#' for x in neighhbour_status]) > 3:
                    new_A[i][j] = "L"
                else:
                    new_A[i][j] = A[i][j]


    return new_A


with open("adventofcode_2020/day11_numbers.txt", "r") as f:
    A = f.read().splitlines()

A = [list(x) for x in A]
new_A = change_state(A)
counter = 0
while A != new_A:
    A = new_A
    print(counter)
    new_A = change_state(A)

    counter += 1

for i in new_A:
    print(''.join(i))

s0 = 0
for i in new_A:
    s0 += ''.join(i).count('#')

print(s0)

"""
Deel 2
"""

def change_state(A):
    n_rows = len(A)
    n_cols = len(A[0])
    new_A = [['.'] * n_cols for _ in range(n_rows)]

    for i in range(n_rows):
        for j in range(n_cols):
            sel_pos = A[i][j]
            if sel_pos == ".":
                new_A[i][j] = "."
            else:
                neighhbour_status = []
                for ii in [-1, 0, 1]:
                    for jj in [-1, 0, 1]:
                        new_i = i + ii
                        new_j = j + jj
                        if new_i == -1 or new_i >= n_rows:
                            continue
                        if new_j == -1 or new_j >= n_cols:
                            continue
                        if ii == 0 and jj == 0:
                            continue
                        # index_to_go[new_i][new_j] += 1
                        neighbour_pos = A[new_i][new_j]
                        neighhbour_status.append(neighbour_pos)
                neighhbour_status = [x for x in neighhbour_status if x != '.']

                if sel_pos == 'L' and not any([x == '#' for x in neighhbour_status]):
                    new_A[i][j] = "#"
                elif sel_pos == '#' and sum([x == '#' for x in neighhbour_status]) > 3:
                    new_A[i][j] = "L"
                else:
                    new_A[i][j] = A[i][j]


    return new_A


with open("adventofcode_2020/day11_numbers.txt", "r") as f:
    A = f.read().splitlines()

A = [list(x) for x in A]


n_rows = len(A)
n_cols = len(A[0])
new_A = [['.'] * n_cols for _ in range(n_rows)]

for i in range(n_rows):
    for j in range(n_cols):
        sel_pos = A[i][j]
        if sel_pos == ".":
            new_A[i][j] = "."
        else:
            # East direction
            max_east = max(n_cols, j + n_cols)
            l_seat = A[i][(j+1):max_east].index('L')
            p_seat = A[i][(j+1):max_east].index('#', False)

            [x[0] for x in A[i]]
            neighhbour_status = []
            for ii in [-1, 0, 1]:
                for jj in [-1, 0, 1]:
                    new_i = i + ii
                    new_j = j + jj
                    if new_i == -1 or new_i >= n_rows:
                        continue
                    if new_j == -1 or new_j >= n_cols:
                        continue
                    if ii == 0 and jj == 0:
                        continue
                    # index_to_go[new_i][new_j] += 1
                    neighbour_pos = A[new_i][new_j]
                    neighhbour_status.append(neighbour_pos)
            neighhbour_status = [x for x in neighhbour_status if x != '.']

            if sel_pos == 'L' and not any([x == '#' for x in neighhbour_status]):
                new_A[i][j] = "#"
            elif sel_pos == '#' and sum([x == '#' for x in neighhbour_status]) > 3:
                new_A[i][j] = "L"
            else:
                new_A[i][j] = A[i][j]

