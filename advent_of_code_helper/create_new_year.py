from advent_of_code_helper.configuration import DDATA_YEAR, DCODE_YEAR, DDEFAULT_DAY
import re
import os
import shutil


def write_new_default_day(day):
    with open(DDEFAULT_DAY, 'r') as f:
        default_day_txt = f.read()

    default_day_txt = re.sub(":day_value:", str(day), default_day_txt)

    with open(file_path, 'w') as f:
        f.write(default_day_txt)

    print(f'\t Written day {ii} to {file_path}')

"""
Create the necessary directories
"""

os.makedirs(DDATA_YEAR, exist_ok=True)
os.makedirs(DCODE_YEAR, exist_ok=True)

"""
Create all the days with a default structure
"""
# Set this variabel to determine from which day on we will generate the default py files
STARTING_DAY = 11
num_days = 25
for ii in range(STARTING_DAY, num_days + 1):
    file_path = os.path.join(DCODE_YEAR, f'day_{ii}.py')
    # Now copy the default...
    if os.path.isfile(file_path):
        print(f"Day {ii} already exists")
        # Default is no
        result = input('Overwrite file? y / [n]') or "n"
        if result == 'y':
            write_new_default_day(ii)
        else:
            print(f'\t Skipped day {ii}')
        print()
    else:
       write_new_default_day(ii)
