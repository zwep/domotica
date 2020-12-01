# encoding: utf-8

import subprocess
from api_secrets import day_1_input

"""
Day 1a
"""

def get_fuel_module(module_mass):
    return int(max(module_mass // 3 - 2, 0))

output = subprocess.check_output(['bash','-c', day_1_input])
input_args = [int(x) for x in output.decode().split()]

res_fuel = sum([get_fuel_module(x) for x in input_args])
print('fuel needed ', res_fuel)

"""
Day 1b
"""

def get_fuel_recursive(mass, total_mass=0):
    temp_fuel_mass = get_fuel_module(mass)

    if temp_fuel_mass != 0:
        total_mass += temp_fuel_mass
        res = get_fuel_recursive(temp_fuel_mass, total_mass)
    else:
        res = total_mass

    return res


res_fuel = sum([get_fuel_recursive(x) for x in input_args])
print('fuel needed ', res_fuel)

