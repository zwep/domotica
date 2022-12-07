import os
import numpy as np
from adventofcode_2022.helper import DPATH

dfile = os.path.join(DPATH, 'day1.txt')
with open(dfile, 'r') as f:
    puzzle_input = f.readlines()

puzzle_input_proc = []
temp_list = []
for i_num in puzzle_input:
    i_num = i_num.strip()
    if i_num.isdigit():
        int_num = int(i_num)
        temp_list.append(int_num)
    else:
        puzzle_input_proc.append(temp_list)
        temp_list = []

# This should also be possible I guess
puzzle_input_proc_2 = [x.split('\n') for x in ''.join(puzzle_input).split('\n\n') if len(x)]

#
sel_input = puzzle_input_proc
sum_input = [sum(x) for x in sel_input]
print('max', max(sum_input))
print('top 3 sum', sum(sorted(sum_input)[-3:]))

sel_input = puzzle_input_proc_2
max([sum([int(y) for y in x]) for x in sel_input])