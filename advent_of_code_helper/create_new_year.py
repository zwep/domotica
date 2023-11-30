from advent_of_code_helper.configuration import DDATA_YEAR, DCODE_YEAR
import re
import os
import shutil

"""
Create the necessary directories
"""

os.makedirs(DDATA_YEAR, exist_ok=True)
os.makedirs(DCODE_YEAR, exist_ok=True)

"""
Create all the days with a default structure
"""

default_day_path = os.path.expanduser('~/PycharmProjects/domotica/advent_of_code_helper/default_day.py')

num_days = 25
for ii in range(num_days + 1):
    file_path = os.path.join(DCODE_YEAR, f'day_{ii}.py')
    # Now copy the default...
    if os.path.isfile(file_path):
        print("File already exists")
        continue
    else:
        with open(default_day_path, 'r') as f:
            default_day = f.read()

        default_day = re.sub(":day_value:", str(ii), default_day)

        with open(file_path, 'w') as f:
            f.write(default_day)