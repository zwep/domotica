import os
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH
import matplotlib.pyplot as plt


dfile = os.path.join(DPATH, 'day10_test.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x.strip() for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if x][::-1]
x0 = 1
signal_strength = []
delay = 0
clock = 100
add_value = 0
while (clock + delay) >= 0:
    if delay > 0:
        delay -= 1
    else:
        x0 += add_value
        if len(puzzle_input):
            i_operation = puzzle_input.pop()
        print(i_operation, clock)

    if i_operation.startswith('addx'):
        add_value = ''.join(re.findall('addx (-|)([0-9]+)', i_operation)[0])
        add_value = int(add_value)
        delay = 1
        i_operation = 'wait'
        clock += 2
    elif i_operation.startswith('noop'):
        add_value = 0
        delay = 0

    clock -= 1
    signal_strength.append(x0)

print(signal_strength)
len(signal_strength)
signal_per_cycle = signal_strength[19::40][:6]
sum([(20 + i * 40) * x for i, x in enumerate(signal_per_cycle)])

"""
Part 2......
"""


dfile = os.path.join(DPATH, 'day10_test.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x.strip() for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if x][::-1]
x0 = 1
signal_strength = []
CRT_output = []
delay = 0
cycle = 0
clock = 100
add_value = 0
while (clock + delay) >= 0:
    if delay > 0:
        delay -= 1
    else:
        x0 += add_value
        if len(puzzle_input):
            i_operation = puzzle_input.pop()
        # print(i_operation, clock)

    if i_operation.startswith('addx'):
        add_value = ''.join(re.findall('addx (-|)([0-9]+)', i_operation)[0])
        add_value = int(add_value)
        delay = 1
        i_operation = 'wait'
        clock += 2
    elif i_operation.startswith('noop'):
        add_value = 0
        delay = 0

    clock -= 1
    signal_strength.append(x0)
    print(cycle, signal_strength[-1]-1, signal_strength[-1]+1)
    if (cycle % 40) in [signal_strength[-1]-1, signal_strength[-1], signal_strength[-1]+1]:
        # CRT_output.append('#')
        CRT_output.append(1)
    else:
        # CRT_output.append('.')
        CRT_output.append(0)

    cycle += 1



print(signal_strength)
len(signal_strength)
signal_per_cycle = signal_strength[19::40][:6]
sum([(20 + i * 40) * x for i, x in enumerate(signal_per_cycle)])
A = np.array(CRT_output[:240]).reshape(6, 40)
import matplotlib.pyplot as plt
plt.imshow(A)