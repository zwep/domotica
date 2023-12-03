import numpy as np
import re
import os
import matplotlib.pyplot as plt
from advent_of_code_helper.helper import read_lines_strip, fetch_data
from advent_of_code_helper.configuration import DDATA_YEAR


def get_num_game(game_line):
    re_num_list = [int(x) for x in re.findall('[0-9]+',game_line)]
    if all([x <= 12 for x in re_num_list]):
        return True
    else:
        return False


def check_game_line(game_line):
    iter_obj = re.finditer("[0-9]+", game_line)
    for i_match_obj in iter_obj:
        # print(i_match_obj)
        nr_dice = int(i_match_obj.group())
        if nr_dice > 12:
            # Now find the color...
            start_id, end_id = i_match_obj.span()
            starting_char = game_line[end_id + 1]
            if nr_dice <= 13 and starting_char == 'g':
                # This is safe
                continue
            elif nr_dice <= 14 and starting_char == 'b':
                # This is also safe
                continue
            else:
                # Violation of the game
                return False
    return True


DAY = "2"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')

# Run get data..
_ = fetch_data(DAY)

# read input
puzzle_input = read_lines_strip(DDATA_DAY)
test_puzzle = ["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
"Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
"Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
"Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
"Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]

possible_game_id = []
for input_line in puzzle_input:
    game_id, game_line = input_line.split(":")
    game_id_int = int(re.findall('[0-9]+', game_id)[0])
    result = get_num_game(game_line)
    if result:
        possible_game_id.append(game_id_int)
    else:
        result_check = check_game_line(game_line)
        if result_check:
            possible_game_id.append(game_id_int)
        else:
            print(game_line)

# 12 red cubes, 13 green cubes, and 14 blue cubes
sum(possible_game_id)

"""

Part 2

"""


def get_minimum_set(game_line):
    re_blue = re.compile("([0-9]+) blue")
    re_red = re.compile("([0-9]+) red")
    re_green = re.compile("([0-9]+) green")
    minimum_blue = max([int(x) for x in re_blue.findall(game_line)])
    minimum_red = max([int(x) for x in re_red.findall(game_line)])
    minimum_green = max([int(x) for x in re_green.findall(game_line)])
    return minimum_green * minimum_red * minimum_blue

puzzle_input = read_lines_strip(DDATA_DAY)
test_puzzle = ["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
"Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
"Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
"Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
"Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]


total_sum = 0
for input_line in puzzle_input:
    game_id, game_line = input_line.split(":")
    game_id_int = int(re.findall('[0-9]+', game_id)[0])
    power_value = get_minimum_set(game_line)
    total_sum += power_value

print(total_sum)