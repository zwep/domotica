import numpy as np
import os
import sys

with open("adventofcode_2020/day8_numbers.txt", "r") as f:
    A = f.read().splitlines()

accumulator = 0
places_visited = []
on = True
counter = 0
while on:
    places_visited.append(counter)

    action, number = A[counter].split()
    if action == "acc":
        accumulator = eval('{accumulator}{operation}{increment}'.format(accumulator=accumulator,
                                                operation=number[0], increment=number[1:]))
        counter += 1
    elif action == "jmp":
        counter = eval('{counter}{operation}{increment}'.format(counter=counter, operation=number[0], increment=number[1:]))
    elif action == "nop":
        counter += 1

    if counter in places_visited:
        on = False

print(accumulator)

"""
Deel 2
"""


with open("adventofcode_2020/day8_numbers.txt", "r") as f:
    A = f.read().splitlines()

def run_zeh_program(A):
    accumulator = 0
    places_visited = []
    on = True
    nice_end = False
    counter = 0
    while on:
        places_visited.append(counter)

        try:
            action, number = A[counter].split()
            if action == "acc":
                accumulator = eval('{accumulator}{operation}{increment}'.format(accumulator=accumulator,
                                                        operation=number[0], increment=number[1:]))
                counter += 1
            elif action == "jmp":
                counter = eval('{counter}{operation}{increment}'.format(counter=counter, operation=number[0], increment=number[1:]))
            elif action == "nop":
                counter += 1

            if counter in places_visited:
                on = False
        except IndexError:
            on = False
            nice_end = True

    return accumulator, nice_end, places_visited

import re
A_copy = np.copy(A)
jmp_index = [i for i, x in enumerate(A_copy) if x.startswith('jmp')]
nop_index = [i for i, x in enumerate(A_copy) if x.startswith('nop')]

for i_jump in jmp_index:
    A_copy = np.copy(A)
    A_copy[i_jump] = re.sub('jmp', 'nop', A_copy[i_jump])
    acc, run_bin, places_visited = run_zeh_program(A_copy)
    if run_bin:
        print(acc)

for i_nop in nop_index:
    A_copy = np.copy(A)
    A_copy[i_nop] = re.sub('nop', 'jmp', A_copy[i_nop])
    acc, run_bin, _ = run_zeh_program(A_copy)
    if run_bin:
        print(acc)
