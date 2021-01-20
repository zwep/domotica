
import sys
import numpy as np
import scipy.signal


def print_output(x):
    x = x.astype(str)
    x[x == '0'] = ','
    x[x == '1'] = '#'
    zz = [[''.join(z) for z in y] for y in x]
    for i in zz:
        print('\n'.join(i))
        print()


day = 17
with open(f"adventofcode_2020/day{str(day)}_numbers.txt", "r") as f:
    A = f.read().splitlines()

# Convert to binary matrix
A = np.array([list(x) for x in A])
A[A == '.'] = 0
A[A == '#'] = 1
A = A.astype(int)

# Create initial cube
B = np.zeros((A.shape[0],) + A.shape, dtype=int)
B[1] = A

# Create neighbour kernel
kernel = np.ones((3, 3, 3), dtype=int)
kernel[1, 1, 1] = 0

# Calculate neighbours..
for i in range(6):
    print(i)
    C = scipy.signal.convolve(B, kernel)
    B = np.pad(B, ((1, 1), (1, 1), (1, 1)))
    B_new = np.zeros(B.shape, dtype=int)
    B_new[(B==0) * (C==3)] = 1
    B_new[(B==1) * ((C==3) + (C==2))] = 1
    B = np.copy(B_new)
    print(i, B.sum())


""" Part 2"""

day = 17
with open(f"adventofcode_2020/day{str(day)}_numbers.txt", "r") as f:
    A = f.read().splitlines()


# Convert to binary matrix
A = np.array([list(x) for x in A])
A[A == '.'] = 0
A[A == '#'] = 1
A = A.astype(int)


B = np.zeros((A.shape[0], A.shape[0]) + A.shape, dtype=int)
B[1, :, :, 1] = A

import scipy.signal
kernel = np.ones((3, 3, 3, 3), dtype=int)
kernel[1, 1, 1, 1] = 0

for i in range(6):
    print(i)
    C = scipy.signal.convolve(B, kernel)
    B = np.pad(B, ((1, 1), (1, 1), (1, 1), (1,1)))
    B_new = np.zeros(B.shape, dtype=int)
    B_new[(B==0) * (C==3)] = 1
    B_new[(B==1) * ((C==3) + (C==2))] = 1
    # B_new[(B==1) * ((C==1) + (C>3))] = 0
    B = np.copy(B_new)
    # print(B)
    # print_output(B)
    print(i, B.sum())
