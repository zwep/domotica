import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR

conv_dict = {False: '-low-', True: '-high-'}


class Module:
    def __init__(self, name, dest_modules):
        self.name = name
        self.dest_modules = dest_modules
        self.state = False
        self.state_dict = None

    def send(self, received_signal, received_module_name):
        """
        :param received_signal: False or True
        :param received_module_name:
        :return:
        """
        raise NotImplementedError


class ButtonTest:
    def __init__(self, module_dict):
        self.module_dict = module_dict
        self.low_high_counter = [0, 0]
        self.global_counter = 0
        self.global_local_counter = 0

        """Ehm okee... hoe groot en diep zitten de conj modules..?"""
        self.conj_module_dict = {k: v for k, v in module_dict.items() if v.state_dict is not None}

        self.current_count = [[sum(v.state_dict.values()) for k, v in self.conj_module_dict.items()]]

    def push_button(self, verbose=False):
        process_signal = [('None', 'button', False)]

        self.global_counter += 1

        while len(process_signal):
            # Get the current module
            source_module_name, target_module_name, signal_to_send = process_signal.pop(0)
            module_obj = self.module_dict.get(target_module_name, None)
            if module_obj:  # This is because... we have an output module..
                next_signals_to_process = module_obj.send(received_signal=signal_to_send, received_module_name=source_module_name)
                if next_signals_to_process:
                    process_signal.extend(next_signals_to_process)
                    for isource, itarget, pulse_type in next_signals_to_process:
                        self.low_high_counter[pulse_type] += 1
                        self.current_count.append([sum(v.state_dict.values()) for k, v in self.conj_module_dict.items()])
                        self.global_local_counter += 1
                        if sum(self.conj_module_dict['hf'].state_dict.values()) > 0:
                            print(self.conj_module_dict['hf'].state_dict.items(), self.global_counter, self.global_local_counter, end='\n\n')
                        if verbose:
                            print(f'{isource} {conv_dict[pulse_type]} -> {itarget}')



class Button(Module):
    def send(self, received_signal, received_module_name=None):
        return [(self.name, 'broadcaster', False)]


class Broadcaster(Module):
    def send(self, received_signal, received_module_name):
        return [(self.name, i_module, received_signal) for i_module in self.dest_modules]


class FlipFlop(Module):
    def send(self, received_signal, received_module_name):
        if received_signal:
            pass
        else:  # It the received signal is low... (False)
            # Then send the inverse of the own state
            pulse_to_send = [(self.name, i_module, not self.state) for i_module in self.dest_modules]
            # And set the inverted state
            self.state = not self.state
            return pulse_to_send


class Conjunction(Module):
    def __init__(self, dest_modules, name, input_modules):
        super().__init__(dest_modules=dest_modules, name=name)
        self.state_dict = {k: False for k in input_modules}

    def send(self, received_signal, received_module_name):
        self.state_dict[received_module_name] = received_signal
        if all(list(self.state_dict.values())):
            pulse_to_send = [(self.name, i_module, False) for i_module in self.dest_modules]
        else:
            pulse_to_send = [(self.name, i_module, True) for i_module in self.dest_modules]
        return pulse_to_send


def get_conjunction_input_module_dict(conjunction_module_names, selected_puzzle):
    conjunction_input_module_dict = {}
    # For each line...
    for i_line in selected_puzzle:
        module_name, destination_list = i_line.split(" -> ")
        module_name_stripped = get_stripped_name(module_name)
        # For each conjunction module name
        for i_conjunction in conjunction_module_names:
            conjunction_input_module_dict.setdefault(i_conjunction, [])
            if i_conjunction in destination_list:
                conjunction_input_module_dict[i_conjunction].append(module_name_stripped)

    return conjunction_input_module_dict


def get_stripped_name(module_name):
    return module_name.strip(flipflop_symbol).strip(conjunction_symbol)


DAY = "20"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

selected_puzzle = puzzle_input
# Flip/flop (%)
flipflop_symbol = '%'
# Conjunction (&)
conjunction_symbol = '&'

# Find all conjunction names... then find which modules SEND to that module.
conjunction_module_names = [x.split(" -> ")[0][1:] for x in selected_puzzle if conjunction_symbol in x]
conjunction_input_module_dict = get_conjunction_input_module_dict(conjunction_module_names, selected_puzzle=selected_puzzle)
button_module = Button(name='button', dest_modules=['broadcaster'])
# Retrieve all modules
module_dict = {'button': button_module}
for i_line in selected_puzzle:
    module_name, destination_names = i_line.split(" -> ")
    destination_list = destination_names.split(", ")
    module_name_stripped = get_stripped_name(module_name)
    if flipflop_symbol in module_name:
        module_obj = FlipFlop(name=module_name_stripped, dest_modules=destination_list)
    elif conjunction_symbol in module_name:
        input_modules = conjunction_input_module_dict[module_name_stripped]
        module_obj = Conjunction(name=module_name_stripped, dest_modules=destination_list, input_modules=input_modules)
    else:
        module_obj = Broadcaster(name=module_name_stripped, dest_modules=destination_list)

    module_dict.update({module_name_stripped: module_obj})

# Ehmm.. so is it OK like this..?
# I need to send a copy
import copy

button_test_obj = ButtonTest(copy.deepcopy(module_dict))
for _ in range(1000):
    button_test_obj.push_button()

button_test_obj.low_high_counter[0] * button_test_obj.low_high_counter[1]

# 807069600
"""
Deel 2..

Dus we moeten
"""


# We know that this is a conjunction...
# Dus als Rx een 'low' moet krijgen... dan moet heel zijn SateDict true zijn...
# Die begint allemaal op low...
# Dus hoe gaan die periodes...?
# Eeeehmm... okee...
button_test_obj = ButtonTest(copy.deepcopy(module_dict))

counter = 0
while counter < 5000:
    button_test_obj.push_button(False)
    counter += 1


z_array = np.array(button_test_obj.current_count)
fig, ax = plt.subplots(1, 5)
ax = ax.ravel()
all_key_names = list(button_test_obj.conj_module_dict.keys())
sel_key_names = ['hf'] + list(button_test_obj.conj_module_dict['hf'].state_dict.keys())
arg_index = [i for i, x in enumerate(all_key_names) if x in sel_key_names]
for i, iax in enumerate(ax):
    ii = arg_index[i]
    iax.plot(z_array[:, ii] / len(button_test_obj.conj_module_dict[all_key_names[ii]].state_dict) * 100)
    iax.set_title(all_key_names[ii])
    iax.set_ylim(0, 110)


# VD: 238704
# TX: 238924
# PC: 246070
# ND: 254862

VD = 3767  # 238704
TX = 3769  # 238924
PC = 3881  # 246070
ND = 4019 # 254862

import math
# Too high..
math.lcm(math.lcm(math.lcm(VD, TX), PC), ND)

# 987608569080 -- too low...
# 221453937522197