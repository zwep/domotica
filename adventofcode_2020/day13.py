
day = 13
with open(f"adventofcode_2020/day{str(day)}_numbers.txt", "r") as f:
    A = f.read().splitlines()


T0 = int(A[0])
active_busses = [int(x) for x in A[1].split(',') if x != 'x']
result = [T0 - (T0 // x + 1) * x for x in active_busses]
import numpy as np

ind_max = np.argmax(result)
abs(result[ind_max]) * active_busses[ind_max]



# Dag 2


day = 13
with open(f"adventofcode_2020/day{str(day)}_numbers.txt", "r") as f:
    A = f.read().splitlines()

T0 = int(A[0])
active_busses = [(int(i), int(x)) for i, x in enumerate(A[1].split(',')) if x != 'x']
offset_m, time_t = zip(*active_busses)
n_busses = len(offset_m)
import numpy as np
b = np.array(offset_m)
A = np.diag(np.array(time_t[1:]), 1)
A[:, 0] = -time_t[0]
import scipy.sparse.linalg
scipy.sparse.linalg.cg(A, b, x0=[100000] * n_busses)
np.linalg.solve(A, b)