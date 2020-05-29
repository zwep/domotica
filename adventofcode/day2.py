# encoding: utf-8

import subprocess
from api_secrets import day_2_input


"""
Day 2a
"""

op_code = [1, 2, 99]
# 99 is halt
# 1 is add positions
# 2 is  multpliply posiions
output = subprocess.check_output(['bash','-c', day_2_input])
input_args = [int(x) for x in output.decode().split(',')]
input_args[1] = 12
input_args[2] = 9

for index in range(0, len(input_args), 4):
    op = input_args[index]
    if op == 99:
        break
    elif op == 1:
        input_args[input_args[index + 3]] = input_args[input_args[index + 1]] + input_args[input_args[index + 2]]
    elif op == 2:
        input_args[input_args[index + 3]] = input_args[input_args[index + 1]] * input_args[input_args[index + 2]]
    else:
        print("The Elves died")


print('output command', input_args[0])

"""
Day 2b
"""

op_code = [1, 2, 99]
# 99 is halt
# 1 is add positions
# 2 is  multpliply posiions
output = subprocess.check_output(['bash','-c', day_2_input])

import matplotlib.pyplot as plt
import numpy as np

noun_0 = 0
verb_0 = 0
goal = 19690720
noun_temp = noun_0
verb_temp = verb_0
history = []
loss_hist = []
for noun_temp in range(100):
    for verb_temp in range(100):
        input_args = [int(x) for x in output.decode().split(",")]
        input_args[1] = noun_temp
        input_args[2] = verb_temp

        for index in range(0, len(input_args), 4):
            op = input_args[index]
            if op == 99:
                break
            elif op == 1:
                input_args[input_args[index + 3]] = input_args[input_args[index + 1]] + input_args[input_args[index + 2]]
            elif op == 2:
                input_args[input_args[index + 3]] = input_args[input_args[index + 1]] * input_args[input_args[index + 2]]
            else:
                print("The Elves died")


        difference = input_args[0] - goal
        if difference == 0:
            print('We have done it!', noun_temp, verb_temp)
            print('res arg', input_args[0], (10 - len(str(input_args[0]))) * ' ', noun_temp, verb_temp)
            pro_noun = noun_temp
            pro_verb = verb_temp
            break

        history.append((noun_temp, verb_temp))
        loss_hist.append(difference)

fig, ax = plt.subplots(2, 1)
ax[0].plot(history)
ax[1].plot(loss_hist)

print(100 * pro_noun + pro_verb)
