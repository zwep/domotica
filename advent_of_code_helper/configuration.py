import os

"""
Here we are going to define the paths.. there wont be much
"""

YEAR = "2022"
DDATA = os.path.expanduser('~/Documents/data/aoc')
DCODE = os.path.expanduser('~/PycharmProjects/domotica')

# Create data directory for the year
DDATA_YEAR = os.path.join(DDATA, YEAR)

# Create code directory for the year
DCODE_YEAR = os.path.join(DCODE, 'adventofcode_' + str(YEAR))

DDEFAULT_DAY = os.path.expanduser('~/PycharmProjects/domotica/advent_of_code_helper/default_day.py')
