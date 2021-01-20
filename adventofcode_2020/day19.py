
import re
import numpy as np
day = 19
with open(f"adventofcode_2020/day{str(day)}_numbers.txt", "r") as f:
    A = f.read().splitlines()

split_index = A.index('')
rules = A[:split_index]
messages = A[split_index+1:]

rules