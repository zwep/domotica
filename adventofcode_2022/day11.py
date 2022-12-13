import os
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH
import matplotlib.pyplot as plt


class Monkey:
    def __init__(self, name, item_worry_list, eval_operation, test_case, reward_true, reward_false):
        self.name = name
        self.item_worry_list = item_worry_list
        self.eval_operation = eval_operation
        self.test_case = test_case
        self.reward_true = reward_true
        self.reward_false = reward_false
        self.number_of_inspections = 0

    def inspect_item(self, worry_level):
        # Necessary to start 'eval'
        old = worry_level
        return eval(self.eval_operation)

    def test_item(self, worry_level):
        if worry_level % self.test_case == 0:
            return self.reward_true
        else:
            return self.reward_false

    def print(self):
        print(f'Monkey {self.name}')
        print(f'Eval operation {self.eval_operation}')
        print(f'\t If true.. {self.reward_true}')
        print(f'\t If false.. {self.reward_false}')
        print('Items ')
        for ii in self.item_worry_list:
            print(f'\t {ii}')
        print('Number of inspections ', self.number_of_inspections)


class Game:
    def __init__(self, monkey_obj_list, player_obj, debug=False):
        # Make sure that they  are sorted...
        self.monkey_object_list = sorted(monkey_obj_list, key=lambda x: x.name)
        self.player_obj = player_obj
        self.debug = debug

    def take_a_round(self):
        for i, x in enumerate(self.monkey_object_list):
            self.take_turn(x)

    def take_turn(self, monkey_object):
        n_items = len(monkey_object.item_worry_list)
        for ii in range(n_items):
            monkey_object.number_of_inspections += 1
            i_worry = monkey_object.item_worry_list.pop(0)
            # Inspect item number ii
            i_worry_test = monkey_object.inspect_item(i_worry % monkey_object.test_case)
            i_worry = monkey_object.inspect_item(i_worry)
            # Reduce worry level after inspection was OK
            # Only for part 1...
            # i_worry = i_worry // 3
            # Test item ii
            throw_to_monkey = monkey_object.test_item(i_worry_test)
            # Throw item
            receiving_monkey = [x for x in self.monkey_object_list if x.name == throw_to_monkey][0]
            receiving_monkey.item_worry_list.append(i_worry % np.prod([x.test_case for x in self.monkey_object_list]))
            if self.debug:
                print(f'Item worry level {i_worry}. Thrown to monkey {receiving_monkey.name}')


def process_input(puzzle_input):
    monkey_str_list = []
    temp_list = []
    for i_line in puzzle_input:
        if i_line == '':
            monkey_str_list.append(temp_list)
            temp_list = []
        else:
            temp_list.append(i_line)

    return monkey_str_list


def string2monkey(monkey_string):
    monkey_number = int(re.findall('Monkey ([0-9]+):', monkey_string[0])[0])
    starting_items_str = re.findall('Starting items: ([0-9]+.*)', monkey_string[1])[0]
    starting_items = list(map(int, starting_items_str.split(',')))
    eval_operation = re.findall('new = (old .*)', monkey_string[2])[0]
    divisible_by = int(re.findall('Test: divisible by ([0-9]+)', monkey_string[3])[0])
    if_true = int(re.findall('monkey ([0-9]+)', monkey_string[4])[0])
    if_false = int(re.findall('monkey ([0-9]+)', monkey_string[5])[0])

    monkey_obj = Monkey(name=monkey_number, item_worry_list=starting_items, eval_operation=eval_operation,
                        test_case=divisible_by, reward_true=if_true, reward_false=if_false)
    return monkey_obj



dfile = os.path.join(DPATH, 'day11.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x.strip() for x in f.readlines()]


monkey_string = process_input(puzzle_input)
monkey_obj_list = [string2monkey(x) for x in monkey_string]

# game_obj = Game(monkey_obj_list, player_obj=None, debug=True)
# # Test a single monkey
# # monkey_obj_list[0].print()
# # game_obj.take_turn(monkey_obj_list[0])
# # monkey_obj_list[0].print()
# for _ in range(20):
#     game_obj.take_a_round()
#
# [x.number_of_inspections for x in monkey_obj_list]
#
# np.prod([x.number_of_inspections for x in sorted(game_obj.monkey_object_list, key= lambda x: x.number_of_inspections)[-2:]])

"""
part 2
"""

monkey_string = process_input(puzzle_input)
monkey_obj_list = [string2monkey(x) for x in monkey_string]

game_obj = Game(monkey_obj_list, player_obj=None, debug=False)
for iround in range(10000):
    if (iround % 1000 == 0) or (iround == 1) or (iround == 20):
        print(iround)
        print([x.number_of_inspections for x in game_obj.monkey_object_list])
    game_obj.take_a_round()

np.prod([x.number_of_inspections for x in sorted(game_obj.monkey_object_list, key= lambda x: x.number_of_inspections)[-2:]])
