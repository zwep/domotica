import numpy as np
import copy
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

    def __init__(self, ore_cost: List):
        # Define 1 ore machine
        self.machine_inventory = dict(zip(self.mineral_name, [0] * len(self.mineral_name)))
        self.machine_inventory['ore'] = 1
        # Define zero inventory
        self.mineral_inventory = dict(zip(self.mineral_name, [0] * len(self.mineral_name)))
        # Machine to action converter
        self.machine2int = dict(zip(self.mineral_name, range(1, len(self.mineral_name) + 1)))
        # Int to machine
        self.int2machine = dict(zip(range(1, len(self.mineral_name) + 1), self.mineral_name))

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


blue_print_1 = [[4, 0, 0, 0], [2, 0, 0, 0], [3, 14, 0, 0], [2, 0, 7, 0]]
creator_obj = OreMachineCreator(blue_print_1)


def run(obj: OreMachineCreator, time=24):
    global MAX_GEODE
    if obj.mineral_inventory['geode'] > MAX_GEODE:
        MAX_GEODE = obj.mineral_inventory['geode']
    if time > 0:
        possible_actions = obj.get_possible_actions()
        for i_action in possible_actions:
            temp_obj = copy.deepcopy(obj)
            temp_obj.execute_action(i_action)
            temp_obj.generate()
            # To score above 0 we require at least A geode machine
            # This is only possible if at the time (remaining) that is equal to the number of obsidian required for a geode machine
            # We still DONT have a obsidian machine, we are screwed.
            geode_obsidian_cost = obj.machine_cost['geode'][2]
            time_geode_obsidian_cost = int((2 * geode_obsidian_cost) ** 0.5)
            # time_geode_obsidian_cost = geode_obsidian_cost
            obsidian_clay_cost = obj.machine_cost['obsidian'][1]
            time_obsidian_clay_cost = int((2 * obsidian_clay_cost) ** 0.5 + time_geode_obsidian_cost)
            # time_obsidian_clay_cost = obsidian_clay_cost + time_geode_obsidian_cost
            clay_ore_cost = obj.machine_cost['clay'][0]
            time_clay_ore_cost = int((2 * clay_ore_cost) ** 0.5 + time_obsidian_clay_cost)
            # time_clay_ore_cost = clay_ore_cost + time_obsidian_clay_cost
            if time == time_geode_obsidian_cost:
                if temp_obj.machine_inventory['obsidian'] == 0:
                    # print(temp_obj.machine_inventory['clay'])
                    return
            if time == time_obsidian_clay_cost:
                if temp_obj.machine_inventory['clay'] == 0:
                    return
            if time == time_clay_ore_cost:
                if temp_obj.machine_inventory['ore'] == 0:
                    return
            # This removed answers...
            # obsidian_clay_cost = obj.machine_cost['obsidian'][1]
            # if time == (geode_obsidian_cost + 1):
            #     if temp_obj.mineral_inventory['clay'] < obsidian_clay_cost:
            #         return
            # Dit werkt ook nog niet
            # if obj.machine_inventory['geode'] > 0:
            #     if obj.machine_inventory['geode'] * time < MAX_GEODE:
            #         return
            run(temp_obj, time-1)


import time


MAX_GEODE = 0
z = time.time()
run(creator_obj, time=16)
print(MAX_GEODE, time.time() - z)
