# encoding: utf-8


import matplotlib.pyplot as plt
import numpy as np
import subprocess
from api_secrets import day_7_input

print('Starting')


def convert_index2mode(x, index, op_mode):
    temp = index
    for _ in range(op_mode+1):
        temp = x[temp]

    return temp


def ACS(input_args, input_list):
    last_output = 0
    input_ind = 0
    n = len(input_args)
    current_index = 0
    # current_index = 2
    op_mode_list = [0] * 10
    op = input_args[current_index]

    while current_index < n:
        n_str = len(str(input_args[current_index:current_index + 3]))
        # print(current_index, input_args[current_index:current_index + 3], (25 - n_str) * ' ', op, op_mode_list)
        if op == 99:
            break
        elif op == 1:
            parameter_index_1 = convert_index2mode(input_args, current_index + 1, op_mode=1-op_mode_list[0])
            parameter_index_2 = convert_index2mode(input_args, current_index + 2, op_mode=1-op_mode_list[1])
            output_index = convert_index2mode(input_args, current_index + 3, op_mode=0)  # We want to get its VALUE
            current_index += 4

            input_args[output_index] = parameter_index_1 + parameter_index_2  # To be used as a location
        elif op == 2:
            parameter_index_1 = convert_index2mode(input_args, current_index + 1, op_mode=1-op_mode_list[0])
            parameter_index_2 = convert_index2mode(input_args, current_index + 2, op_mode=1-op_mode_list[1])
            output_index = convert_index2mode(input_args, current_index + 3, op_mode=0)
            current_index += 4
            input_args[output_index] = parameter_index_1 * parameter_index_2
        elif op == 3:
            output_index = convert_index2mode(input_args, current_index + 1, op_mode=0)
            print(input_list)
            temp_input = int(input_list[input_ind])
            input_ind += 1
            input_args[output_index] = temp_input
            current_index += 2
        elif op == 4:
            output = convert_index2mode(input_args, current_index + 1, op_mode=1 - op_mode_list[0])
            current_index += 2
            # print('\t op code 4', output)
            last_output = output
        elif op == 5 :
            # Day 5b
            non_zero_int = convert_index2mode(input_args, current_index + 1, op_mode=1 - op_mode_list[0])
            new_index = convert_index2mode(input_args, current_index + 2, op_mode=1 - op_mode_list[1])
            if non_zero_int > 0:
                current_index = new_index
            else:
                current_index += 3
        elif op == 6 :
            zero_int = convert_index2mode(input_args, current_index + 1, op_mode=1 - op_mode_list[0])
            new_index = convert_index2mode(input_args, current_index + 2, op_mode=1 - op_mode_list[1])
            if zero_int == 0:
                current_index = new_index
            else:
                current_index += 3
        elif op == 7 :
            parameter_index_1 = convert_index2mode(input_args, current_index + 1, op_mode=1 - op_mode_list[0])
            parameter_index_2 = convert_index2mode(input_args, current_index + 2, op_mode=1 - op_mode_list[1])
            parameter_index_3 = convert_index2mode(input_args, current_index + 3, op_mode=0)  # Write parameter
            if parameter_index_1 < parameter_index_2:
                input_args[parameter_index_3] = 1
            else:
                input_args[parameter_index_3] = 0

            current_index += 4

        elif op == 8 :
            parameter_index_1 = convert_index2mode(input_args, current_index + 1, op_mode=1 - op_mode_list[0])
            parameter_index_2 = convert_index2mode(input_args, current_index + 2, op_mode=1 - op_mode_list[1])
            parameter_index_3 = convert_index2mode(input_args, current_index + 3, op_mode=0)  # Write parameter
            if parameter_index_1 == parameter_index_2:
                input_args[parameter_index_3] = 1
            else:
                input_args[parameter_index_3] = 0
            current_index += 4

        elif op > 99:
            temp_op_mode = list(str(op))[:-2]
            for i_index, i_mode in enumerate(temp_op_mode[::-1]):
                op_mode_list[i_index] = int(i_mode)

            op = int(str(op)[-2:])
            continue
        else:
            print("The Elves died")
            break

        # Reset mode list and get the next op
        op_mode_list = [0] * 10
        op = input_args[current_index]

    return last_output
#
#
# output = subprocess.check_output(['bash', '-c', day_7_input])
# input_args = [x.split(',') for x in output.decode().split('\n')]
# input_args = [int(x) for x in input_args[0]]
#
# print('Starting')
# import itertools
# range_amp = [0, 1, 2, 3, 4]
# res = []
# for int_1, int_2, int_3, int_4, int_5 in itertools.permutations(range_amp):
#
#     output_1 = ACS(input_args, [int_1, 0])
#     output_2 = ACS(input_args, [int_2, output_1])
#     output_3 = ACS(input_args, [int_3, output_2])
#     output_4 = ACS(input_args, [int_4, output_3])
#     output_5 = ACS(input_args, [int_5, output_4])
#     res.append(output_5)
#
# import matplotlib.pyplot as plt
# plt.plot(res)
# np.max(res)
# list(itertools.permutations(range_amp))[115]

"""
Day b
"""

output = subprocess.check_output(['bash', '-c', day_7_input])
input_args = [x.split(',') for x in output.decode().split('\n')]
input_args = [int(x) for x in input_args[0]]

print('Starting')
import itertools

ACS(input_args, [5, 2])

range_amp = list(range(5, 10))
res = []
for int_1, int_2, int_3, int_4, int_5 in itertools.permutations(range_amp):
    output_5 = 0
    counter = 0
    while counter < 1000:
        counter += 1
        output_1 = ACS(input_args, [5, output_5])
        output_2 = ACS(input_args, [int_2, output_1])
        output_3 = ACS(input_args, [int_3, output_2])
        output_4 = ACS(input_args, [int_4, output_3])
        output_5 = ACS(input_args, [int_5, output_4])
        res.append(output_5)

import matplotlib.pyplot as plt

plt.plot(res)
np.max(res)
list(itertools.permutations(range_amp))[115]