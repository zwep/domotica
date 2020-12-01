# encoding: utf-8

import numpy as np
import os
import matplotlib.pyplot as plt

"""
Day 4 a
"""

lower_bound = 134564
upper_bound = 585159

# 6 digit number
x1 = lower_bound
result_number = []
while x1 < upper_bound:
    x1 += 1
    x1_temp = np.array(list(str(x1))).astype(int)

    if np.any(np.diff(x1_temp) < 0):
        continue
    else:
        if np.all(np.diff(x1_temp) != 0):
            continue
        else:
            result_number.append(x1)

len(result_number)

"""
Day 4b
"""

sel_number = []
for x1 in result_number:
    x1_temp = np.array(list(str(x1))).astype(int)

    prev_item = x1_temp[0]
    index_list = []
    for i, i_item in enumerate(x1_temp[1:]):
        if i_item == prev_item:
            pass
        else:
            index_list.append(i+1)
            prev_item = i_item

    x1_bool_split = np.split(x1_temp, index_list)
    conseq_true = [len(x) for x in x1_bool_split if np.all(x)]
    if np.any(np.array(conseq_true) == 2):
        sel_number.append(x1)

len(sel_number)
