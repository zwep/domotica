import os
from advent_of_code_helper.configuration import YEAR, DDATA_YEAR


def read_lines(file_path):
    with open(file_path, 'r') as f:
        content = f.readlines()
    return content


def fetch_data(day):
    ddata_day = os.path.join(DDATA_YEAR, day + '.txt')
    if os.path.isfile(ddata_day):
        return -1
    else:
        fetch_data = f"aocdl -day {day} -year {YEAR} -output {ddata_day}"
        os.system(fetch_data)
        return 1
