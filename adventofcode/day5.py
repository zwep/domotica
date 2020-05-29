# encoding: utf-8


import matplotlib.pyplot as plt
import numpy as np
import subprocess
from api_secrets import day_5_input

print('Starting')


def convert_index2mode(x, index, op_mode):
    temp = index
    for _ in range(op_mode+1):
        temp = x[temp]

    return temp

# 99 is halt
# 1 is add positions
# 2 is  multpliply posiions
# 3 is move position
# 4 is print position...


# output = subprocess.check_output(['bash', '-c', day_5_input])
# input_args = [x.split(',') for x in output.decode().split('\n')]
input_args = np.array([['3', '225', '1', '225', '6', '6', '1100', '1', '238', '225', '104', '0', '1002', '148', '28', '224', '1001', '224', '-672', '224', '4', '224', '1002', '223', '8', '223', '101', '3', '224', '224', '1', '224', '223', '223', '1102', '8', '21', '225', '1102', '13', '10', '225', '1102', '21', '10', '225', '1102', '6', '14', '225', '1102', '94', '17', '225', '1', '40', '173', '224', '1001', '224', '-90', '224', '4', '224', '102', '8', '223', '223', '1001', '224', '4', '224', '1', '224', '223', '223', '2', '35', '44', '224', '101', '-80', '224', '224', '4', '224', '102', '8', '223', '223', '101', '6', '224', '224', '1', '223', '224', '223', '1101', '26', '94', '224', '101', '-120', '224', '224', '4', '224', '102', '8', '223', '223', '1001', '224', '7', '224', '1', '224', '223', '223', '1001', '52', '70', '224', '101', '-87', '224', '224', '4', '224', '1002', '223', '8', '223', '1001', '224', '2', '224', '1', '223', '224', '223', '1101', '16', '92', '225', '1101', '59', '24', '225', '102', '83', '48', '224', '101', '-1162', '224', '224', '4', '224', '102', '8', '223', '223', '101', '4', '224', '224', '1', '223', '224', '223', '1101', '80', '10', '225', '101', '5', '143', '224', '1001', '224', '-21', '224', '4', '224', '1002', '223', '8', '223', '1001', '224', '6', '224', '1', '223', '224', '223', '1102', '94', '67', '224', '101', '-6298', '224', '224', '4', '224', '102', '8', '223', '223', '1001', '224', '3', '224', '1', '224', '223', '223', '4', '223', '99', '0', '0', '0', '677', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1105', '0', '99999', '1105', '227', '247', '1105', '1', '99999', '1005', '227', '99999', '1005', '0', '256', '1105', '1', '99999', '1106', '227', '99999', '1106', '0', '265', '1105', '1', '99999', '1006', '0', '99999', '1006', '227', '274', '1105', '1', '99999', '1105', '1', '280', '1105', '1', '99999', '1', '225', '225', '225', '1101', '294', '0', '0', '105', '1', '0', '1105', '1', '99999', '1106', '0', '300', '1105', '1', '99999', '1', '225', '225', '225', '1101', '314', '0', '0', '106', '0', '0', '1105', '1', '99999', '108', '677', '677', '224', '102', '2', '223', '223', '1005', '224', '329', '101', '1', '223', '223', '1107', '677', '226', '224', '102', '2', '223', '223', '1006', '224', '344', '101', '1', '223', '223', '1107', '226', '226', '224', '102', '2', '223', '223', '1006', '224', '359', '101', '1', '223', '223', '1108', '677', '677', '224', '102', '2', '223', '223', '1005', '224', '374', '101', '1', '223', '223', '8', '677', '226', '224', '1002', '223', '2', '223', '1005', '224', '389', '101', '1', '223', '223', '108', '226', '677', '224', '1002', '223', '2', '223', '1006', '224', '404', '1001', '223', '1', '223', '107', '677', '677', '224', '102', '2', '223', '223', '1006', '224', '419', '101', '1', '223', '223', '1007', '226', '226', '224', '102', '2', '223', '223', '1005', '224', '434', '101', '1', '223', '223', '1007', '677', '677', '224', '102', '2', '223', '223', '1005', '224', '449', '1001', '223', '1', '223', '8', '677', '677', '224', '1002', '223', '2', '223', '1006', '224', '464', '101', '1', '223', '223', '1108', '677', '226', '224', '1002', '223', '2', '223', '1005', '224', '479', '101', '1', '223', '223', '7', '677', '226', '224', '1002', '223', '2', '223', '1005', '224', '494', '101', '1', '223', '223', '1008', '677', '677', '224', '1002', '223', '2', '223', '1006', '224', '509', '1001', '223', '1', '223', '1007', '226', '677', '224', '1002', '223', '2', '223', '1006', '224', '524', '1001', '223', '1', '223', '107', '226', '226', '224', '1002', '223', '2', '223', '1006', '224', '539', '1001', '223', '1', '223', '1107', '226', '677', '224', '102', '2', '223', '223', '1005', '224', '554', '101', '1', '223', '223', '1108', '226', '677', '224', '102', '2', '223', '223', '1006', '224', '569', '101', '1', '223', '223', '108', '226', '226', '224', '1002', '223', '2', '223', '1006', '224', '584', '1001', '223', '1', '223', '7', '226', '226', '224', '1002', '223', '2', '223', '1006', '224', '599', '101', '1', '223', '223', '8', '226', '677', '224', '102', '2', '223', '223', '1005', '224', '614', '101', '1', '223', '223', '7', '226', '677', '224', '1002', '223', '2', '223', '1005', '224', '629', '101', '1', '223', '223', '1008', '226', '677', '224', '1002', '223', '2', '223', '1006', '224', '644', '101', '1', '223', '223', '107', '226', '677', '224', '1002', '223', '2', '223', '1005', '224', '659', '1001', '223', '1', '223', '1008', '226', '226', '224', '1002', '223', '2', '223', '1006', '224', '674', '1001', '223', '1', '223', '4', '223', '99', '226'], ['']])
input_args = input_args[0]
input_args = [int(x) for x in input_args]
day_b = True

print('Starting')

n = len(input_args)
current_index = 0
# current_index = 2
op_mode_list = [0] * 10
op = input_args[current_index]

while current_index < n:
    n_str = len(str(input_args[current_index:current_index + 3]))
    print(current_index, input_args[current_index:current_index + 3], (25 - n_str) * ' ', op, op_mode_list)
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
        input_args[output_index] = int(input('Please enter some input'))
        current_index += 2
    elif op == 4:
        output = convert_index2mode(input_args, current_index + 1, op_mode=1 - op_mode_list[0])
        current_index += 2
        print('\t op code 4', output)
    elif op == 5 and day_b:
        # Day 5b
        non_zero_int = convert_index2mode(input_args, current_index + 1, op_mode=1 - op_mode_list[0])
        new_index = convert_index2mode(input_args, current_index + 2, op_mode=1 - op_mode_list[1])
        if non_zero_int > 0:
            current_index = new_index
        else:
            current_index += 3
    elif op == 6 and day_b:
        zero_int = convert_index2mode(input_args, current_index + 1, op_mode=1 - op_mode_list[0])
        new_index = convert_index2mode(input_args, current_index + 2, op_mode=1 - op_mode_list[1])
        if zero_int == 0:
            current_index = new_index
        else:
            current_index += 3
    elif op == 7 and day_b:
        parameter_index_1 = convert_index2mode(input_args, current_index + 1, op_mode=1 - op_mode_list[0])
        parameter_index_2 = convert_index2mode(input_args, current_index + 2, op_mode=1 - op_mode_list[1])
        parameter_index_3 = convert_index2mode(input_args, current_index + 3, op_mode=0)  # Write parameter
        if parameter_index_1 < parameter_index_2:
            input_args[parameter_index_3] = 1
        else:
            input_args[parameter_index_3] = 0

        current_index += 4

    elif op == 8 and day_b:
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

