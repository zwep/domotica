import numpy as np
import os
import sys

with open("adventofcode_2020/day9_numbers.txt", "r") as f:
    A = [int(x) for x in f.read().splitlines()]

n_back = 25
final_index = 0
for i in range(n_back+1, len(A)):
    sel_item = A[i]
    prev_items = A[i-n_back:i]
    needed_items = [x for x in prev_items if x < sel_item]
    residual_items = [sel_item - x for x in needed_items]
    found_item = False
    for ix in residual_items:
        if ix in needed_items:
            found_item = True

        if found_item:
            temp_index = needed_items.index(ix)
            # print('We have found something ', sel_item, ix, residual_items[temp_index])
            break
        else:
            continue
    if found_item is False:
        final_index = i


final_value = A[final_index]
for i in range(final_index):
    n_max = 2
    cur_approx = -1
    while cur_approx < final_value:
        n_max += 1
        cur_approx = sum(A[i:n_max])

    if cur_approx == final_value:
        print(i, n_max)
        break

        min(A[400: 417]) + max(A[400: 417])
        A[400] + A[417]