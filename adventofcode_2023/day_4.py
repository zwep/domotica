import numpy as np
import os
import matplotlib.pyplot as plt
import re
from advent_of_code_helper.helper import read_lines_strip, fetch_data, fetch_test_data
from advent_of_code_helper.configuration import DDATA_YEAR


def parse_input(x_str):
    card_str, game_content = x_str.split(':')
    card_id = re.findall('\d+', card_str)
    winning_str, collected_str = game_content.split("|")
    winning_list = set(list(map(int, re.findall('\d+', winning_str))))
    collected_list = set(list(map(int, re.findall('\d+', collected_str))))
    return card_id, winning_list, collected_list


def day2(x_input):
    return None


DAY = "4"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')

# Run get data..
_ = fetch_data(DAY)
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = fetch_data(DAY)
_ = fetch_test_data(DAY)

test_puzzle_input = read_lines_strip(DDATA_DAY_TEST)

input_puzzle = ["Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
"Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
"Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
"Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
"Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
"Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"]
# read input
input_puzzle = read_lines_strip(DDATA_DAY)
s = 0
max_cards = len(input_puzzle)
result_dict = {k: [0, 1] for k in range(1, max_cards+1)}
for i_line in input_puzzle:
    print(result_dict)
    card_id, winning_set, collected_set = parse_input(i_line)
    card_int = int(*card_id)
    result = len(winning_set.intersection(collected_set))
    print(card_int, result)
    if result > 0:
        s += 2 ** (result - 1)
        result_dict[card_int][0] = 2 ** (result - 1)
        # Based on the result, increase the amount of copies
        for i_result in range(1, result+1):
            if card_int + i_result <= max_cards:
                result_dict[card_int + i_result][1] += result_dict[card_int][1]
            else:
                break

# Solution 1
sum([v[0] for k, v in result_dict.items()])
# Solution 2
sum([v[1] for k, v in result_dict.items()])
