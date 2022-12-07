import os
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH


dfile = os.path.join(DPATH, 'day6.txt')
with open(dfile, 'r') as f:
    puzzle_input = f.read()


test_string = puzzle_input

def check_string(x):
    return len(set(list(x))) == 14

result = [(check_string(test_string[i:i+14]), i) for i in range(len(test_string))]
min([x[1] for x in result if x[0]]) + 14
