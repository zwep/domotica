

def get_last_parenthesis(i_line):
    index_last_p = len(i_line) - i_line[::-1].index('(') - 1
    index_interval_p = []
    parenthese_count = 0
    for j, i_sub_char in enumerate(i_line[index_last_p:]):
        if i_sub_char == "(":
            parenthese_count += 1
        if i_sub_char == ")":
            parenthese_count -= 1

        if parenthese_count == 0:
            index_interval_p = [index_last_p, index_last_p + j]
            break
    return index_interval_p


def get_parenthesis_outcome(i_line, index_interval_p):
    # Calculate stuff
    min_char, max_char = index_interval_p
    s0 = eval(''.join(i_line[min_char+1:min_char+4]))
    i_line_sub = i_line[min_char+4:max_char]
    if len(i_line_sub):
        n_size = 2
        chunks = [''.join(i_line_sub[ii:ii+n_size]) for ii in range(0, len(i_line_sub), n_size)]
        for i_chunk in chunks:
            s0 = eval(f"{s0}{i_chunk}")

    i_line[min_char:max_char+1] = [str(s0)]
    return i_line


import re
import numpy as np
day = 18
with open(f"adventofcode_2020/day{str(day)}_numbers.txt", "r") as f:
    A = f.read().splitlines()

total_result = []

for i_line in A:
    i_line = re.sub(' ', '', i_line)
    i_line = list(i_line)

    # Get last parentheses
    while "(" in i_line:
        index_interval_p = get_last_parenthesis(i_line)
        i_line = get_parenthesis_outcome(i_line, index_interval_p)

    result = get_parenthesis_outcome(i_line, [-1, len(i_line)])[-1]
    print(result)
    total_result.append(result)

print('Final result', sum([int(x) for x in total_result]))


"""Deel tweee..."""


def get_parenthesis_outcome_plus(i_line, index_interval_p):
    # Calculate stuff
    min_char, max_char = index_interval_p
    S = i_line[min_char+1: max_char]
    while "+" in S:
        i_plus = S.index('+')
        s0 = eval(''.join(S[i_plus - 1:i_plus+2]))
        S[i_plus - 1:i_plus+2] = [str(s0)]
    # Output of para
    s1 = eval(''.join(S))
    i_line[min_char: max_char+1] = [str(s1)]
    return i_line


total_result = []

for i_line in A:
    i_line = re.sub(' ', '', i_line)
    i_line = list(i_line)
    # Get last parentheses
    while "(" in i_line:
        index_interval_p = get_last_parenthesis(i_line)
        i_line = get_parenthesis_outcome_plus(i_line, index_interval_p)
        print(i_line)

    result = get_parenthesis_outcome_plus(i_line, [-1, len(i_line)])[-1]
    print(result)


    total_result.append(result)

sum([int(x) for x in total_result])
