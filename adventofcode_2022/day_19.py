import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR
from typing import List


def day1(x_input):
    return None


def day2(x_input):
    return None


DAY = "19"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

#
class OreMachineCreator:
    """
    Actions in this Ore Machine Creator are

    0 - wait
    1 - build ore machine
    2 - build clay machine
    3 - build obsidian machine
    4 - build geode machine
    """
    # Every instance should start with this
    mineral_name = ['ore', 'clay', 'obsidian', 'geode']
    # Define 1 ore machine
    machine_inventory = dict(zip(mineral_name, [0] * len(mineral_name)))
    machine_inventory['ore'] = 1
    # Define zero inventory
    mineral_inventory = dict(zip(mineral_name, [0] * len(mineral_name)))
    # Machine to action converter
    machine2int = dict(zip(mineral_name, range(1, len(mineral_name)+1)))
    # Int to machine
    int2machine = dict(zip(range(1, len(mineral_name) + 1, mineral_name)))

    def __init__(self, ore_cost: List):
        # Input order is same as order inside mineral name
        self.machine_cost = dict(zip(self.mineral_name, ore_cost))

    def get_possible_actions(self):
        # Determine which actions are possible...
        possible_action = [0]
        for machine_ore_k, machine_cost_k in self.machine_cost.items():
            # This is a list of ints. For example [14, 2, 0, 0]  (14 ore, 2 clay)
            # Now loop over all mineral names, and check if we satisfy all the constraints
            boolean_cost = [self.mineral_inventory[i_ore] >= machine_cost_k[ii] for ii, i_ore in enumerate(self.mineral_name)]
            if all(boolean_cost):
                action_int = self.machine2int[machine_ore_k]
                possible_action.append(action_int)
        return possible_action

    def generate(self):
        for k, v in self.machine_inventory.items():
            self.mineral_inventory[k] += v

    def execute_action(self, action_index):
        if action_index == 0:
            return
        else:
            machine_str = self.int2machine[action_index]
            self.machine_inventory[machine_str] += 1
            machine_cost = self.machine_cost[machine_str]
            for ii, i_ore in enumerate(self.mineral_name):
                self.mineral_inventory[i_ore] -= machine_cost[ii]

    def run(self)
blue_print_1 = [[4, 0, 0, 0], [2, 0, 0, 0], [3, 14, 0, 0], [2, 0, 7, 0]]
creator_obj = OreMachineCreator(blue_print_1)
creator_obj.get_possible_actions()
creator_obj.generate()
creator_obj.generate()
creator_obj.get_possible_actions()
