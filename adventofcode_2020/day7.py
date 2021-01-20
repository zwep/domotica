import numpy as np
import os
import sys

with open("adventofcode_2020/day7_test.txt", "r") as f:
    A = f.read().splitlines()

import re

key_search = 'shiny gold'
bag_dict = {}
for i_line in A:
    bags = re.findall("(\w+ \w+) bag(?:|s)", i_line)
    bag_dict.update({bags[0]: bags[1:]})


def get_parent_keys(x, key):
    key_list = []
    for k, v in x.items():
        if key in v:
            # counter_set = counter_set.union(set([k]))
            key_list.append(k)
    return key_list


def get_recursive_keys(x, key_list, counter=0, found_keys=None):
    for i_key in key_list:
        new_keys = get_parent_keys(x, i_key)
        print(counter * '\t', i_key, new_keys)
        if len(new_keys) > 0:
            found_keys.extend(new_keys)
            get_recursive_keys(x, new_keys, counter+1, found_keys)

    return found_keys

res = get_recursive_keys(bag_dict, [key_search], 0,  [])
print(len(set(res)))

"""
DAG 2"""

with open("adventofcode_2020/day7_numbers.txt", "r") as f:
    A = f.read().splitlines()

key_search = 'shiny gold'
bag_dict = {}
for i_line in A:
    bags = re.findall("([0-9] |)(\w+ \w+) bag(?:|s)", i_line)
    bag_dict.update({bags[0][1]: bags[1:]})


def multiply_add_count(x, key_search, counter=0):
    temp = 0
    for count, key in x[key_search]:
        if count:
            count = int(count)
            temp += count * multiply_add_count(x, key, counter+1) + count
            print(temp, counter * '-', count, key)
        else:
            print(counter * '\t', 1, key)
            return 0

    return temp

res = multiply_add_count(bag_dict, key_search)
print(res)