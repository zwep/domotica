# encoding: utf-8

import numpy as np
import os
import matplotlib.pyplot as plt
from api_secrets import day_6_input
import subprocess

"""

"""

output = subprocess.check_output(['bash', '-c', day_6_input])
input_args = [x.split(',') for x in output.decode().split('\n')]

import itertools
input_args = [x for x in itertools.chain(*input_args) if len(x)]


def nested_update(x, key, value):
    for k, v in x.items():
        # temp_k == k  # Dan is t object erall.. en hebben we dus een afspliting.
        if key == k:
            x[k].update({value: {}})
            return 1
        else:
            nested_update(x[k], key, value)
    return 0


def nested_correct(x, y, key, res=0):
    for k, v in x.items():
        if key == k:
            # print(key, ' found it! ', end=" ")
            x[k].update(y)
            return 1
        else:
            res = nested_correct(x[k], y, key, res)
    return res


def nested_find(x, key, res=0, prev_key=''):
    for k, v in x.items():
        if key == k:
            print('Found key!', x[k], k)
            print('Prev key', prev_key)
            return 1
        else:
            res = nested_find(x[k], key, res, k)
    return res


def nested_count(x, count=0):
    for k, v in x.items():
        if isinstance(v, dict):
            if len(v):
                count = nested_count(v, count+1)
        else:
            for iv in v:
                count = nested_count(iv, count+1)
    return count


def nested_keys(x, key_list=()):
    for k, v in x.items():
        key_list.append(k)
        if isinstance(v, dict):
            key_list = nested_keys(v, key_list)
        else:
            for iv in v:
                key_list = nested_keys(iv, key_list)
    return key_list


def calc_depth(x, depth=0, total=0):
    total += depth
    for k, v in x.items():
        if isinstance(v, dict):
            if len(v):
                total = calc_depth(v, depth+1, total)
        else:
            print('start')
            depth+=1
            for iv in v:
                total = calc_depth(iv, depth+1, total)
    return total


orbit_dict = {}
for i_orbit in input_args:
    temp_k, temp_v = i_orbit.split(')')
    # Search the dictionary for keys and values...
    res = nested_update(orbit_dict, temp_k, temp_v)
    if res == 0:
        orbit_dict.update({temp_k: {temp_v: {}}})

offset = 0
res_dict = {}
list_keys = sorted(list(orbit_dict.keys()))
n_keys = len(list_keys)

import copy
for i in range(n_keys):
    sel_k = list_keys[i]
    sel_dict = orbit_dict[sel_k]  # substitution value...
    temp_dict = {k: v for k, v in orbit_dict.items() if k != sel_k}
    res = nested_correct(temp_dict, sel_dict, sel_k)
    if res == 0:
        continue
    else:
        orbit_dict = copy.deepcopy(temp_dict)

calc_depth(orbit_dict)
