import numpy as np
import os
import re
import matplotlib.pyplot as plt
import advent_of_code_helper.helper as helper
from advent_of_code_helper.configuration import DDATA_YEAR


def process_fun_list(fun_list, workflow, function_dict, item_dict):
    for i_fun in fun_list:
        eval_fun, fun_result = i_fun.split(":")
        check_condition = re.sub("([a-z])", lambda x: item_dict.get(x.group(1), "error"), eval_fun)
        if eval(check_condition):
            return process_result(fun_result, workflow, function_dict, item_dict)
    else:
        return False, workflow

def process_result(fun_result, workflow, function_dict, item_dict):
    if fun_result in function_dict.keys():
        workflow.append(fun_result)
    else:
        workflow = []
        item_dict['RESULT'] = fun_result
    return True, workflow


def process_workflow_item(item_dict, function_dict, function_default_dict):
    workflow = ["in"]
    while len(workflow):
        print(workflow)
        current_workflow = workflow.pop()
        fun_list = function_dict[current_workflow]
        # Process key...
        ind_continue, workflow = process_fun_list(fun_list, workflow, function_dict, item_dict)
        if ind_continue:
            continue
        else:
            # Process the default value..
            fun_result = function_default_dict[current_workflow]
            process_result(fun_result, workflow, function_dict, item_dict)
    return item_dict


def process_item(current_item_str):
    item_dict = {}
    for i_item in re.sub("{|}", "", current_item_str).split(","):
        i_key, i_value = i_item.split("=")
        item_dict[i_key] = i_value

    return item_dict


def process_input(selected_puzzle):
    space_index = selected_puzzle.index('')
    function_text = selected_puzzle[:space_index]
    input_text = selected_puzzle[space_index + 1:]
    return function_text, input_text

def build_workflow_dict(function_text):
    # Build the function list
    function_dict = {}
    function_default_dict = {}
    for i_function in function_text:
        i_key, i_fun = i_function.split("{")
        i_fun = i_fun.split("}")[0]
        i_fun_list = i_fun.split(",")
        default_value = i_fun_list.pop()
        function_default_dict[i_key] = default_value
        function_dict[i_key] = i_fun_list

    return function_dict, function_default_dict

DAY = "19"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = helper.fetch_data(DAY)
_ = helper.fetch_test_data(DAY)

# read input
puzzle_input = helper.read_lines_strip(DDATA_DAY)
test_puzzle_input = helper.read_lines_strip(DDATA_DAY_TEST)

selected_puzzle = test_puzzle_input

#
function_text, input_text = process_input(selected_puzzle)
function_dict, function_default_dict = build_workflow_dict(function_text)

to_sum = []
for sel_item in input_text:
    item_dict = process_item(sel_item)
    item_dict = process_workflow_item(item_dict, function_dict, function_default_dict)
    if item_dict['RESULT'] == 'A':
        for k, v in item_dict.items():
            if k != 'RESULT':
                to_sum.append(int(v))

print('Part 1 ', sum(to_sum))

"""
Okay lets re-map it

"""


selected_puzzle = puzzle_input
function_text, input_text = process_input(selected_puzzle)
function_dict, function_default_dict = build_workflow_dict(function_text)


invert_dict = {"<": ">=", ">": "<="}


# Find all 'A' positions
def get_IOI_positions(sel_char='A'):
    IOI_position_list = []
    for k, fun_list in function_dict.items():
        for ii, i_fun in enumerate(fun_list):
            # Required because of 'lz' and 'tlz', 'lzx'...
            if (":" + sel_char in i_fun) and not (":" + sel_char + ","in i_fun) :
                print(sel_char, i_fun)
            # if ":" + sel_char in i_fun:
            #     IOI_position_list.append((k, ii))
            if i_fun.endswith(":" + sel_char):
                IOI_position_list.append((k, ii))

    for k, default_value in function_default_dict.items():
        if sel_char == default_value:
            IOI_position_list.append((k, -1))

    return IOI_position_list


def process_inverted_funlist(current_workflow, IOI, inequal_str):
    # Invert everything when we are looking for the last one
    if IOI == -1:
        fun_list = function_dict[current_workflow]
        invert = True
    else:
        fun_list = function_dict[current_workflow][:(IOI+1)]
        invert = False

    for fun_str in fun_list[::-1]:
        condition_str, _ = fun_str.split(":")
        if invert:
            condition_str = re.sub("(<|>)", lambda x: invert_dict.get(x.group(1)), condition_str)
        inequal_str += condition_str + ","
        invert = True
    return inequal_str


def dump(current_workflow, IOI):
    inequal_str = ""
    while len(current_workflow):
        inequal_str = process_inverted_funlist(current_workflow, IOI, inequal_str)
        # Now find where the current_workflow is and update IOI
        current_workflow_list = get_IOI_positions(sel_char=current_workflow)
        if len(current_workflow_list) == 1:
            current_workflow, IOI = current_workflow_list[0]
        else:
            current_workflow = []
    else:
        return inequal_str

IOI_position_list = get_IOI_positions(sel_char='A')


max_range = 4000
min_range = 1

total_s = 0
for ii, i_A_pos in enumerate(IOI_position_list):
    current_workflow, IOI = i_A_pos
    z = dump(current_workflow, IOI)
    # IOI : Index Of Interest
    # print(z)
    s = 1
    for i_letter in ['x', 'm', 'a', 's']:
        letter_conditions = z.split(",")[:-1]
        filtered_letter = [x for x in letter_conditions if i_letter in x]
        if filtered_letter:
            minimum_conditions = [x for x in filtered_letter if '>' in x]
            if len(minimum_conditions):
                minimum_value = 1
                for i_min in minimum_conditions:
                    i_min_value = int(re.findall('([0-9]+)', i_min)[0])
                    # 'Maximize the minimum value when we find one
                    if i_min_value > minimum_value:
                        minimum_value = i_min_value
                        if '>=' in i_min:
                            minimum_value -= 1
            else:
                minimum_value = min_range - 1
            maximum_conditions = [x for x in filtered_letter if '<' in x]
            if len(maximum_conditions):
                maximum_value = max_range
                for i_max in maximum_conditions:
                    i_max_value = int(re.findall('([0-9]+)', i_max)[0])
                    # Reduce the maximum value if we found a lower one...
                    if i_max_value < maximum_value:
                        maximum_value = i_max_value
                        if '<=' in i_max:
                            maximum_value += 1
            else:
                maximum_value = max_range + 1
        else:
            minimum_value = min_range - 1
            maximum_value = max_range + 1

        s *= (maximum_value - minimum_value) - 1
        # print(i_letter, minimum_value, maximum_value, (maximum_value - minimum_value - 1))
    total_s += s
    # print()

print(total_s)
# TOO HIGH 10231034101346944
#            132380153677887
