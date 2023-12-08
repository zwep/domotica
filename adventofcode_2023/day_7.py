import numpy as np
import os
import re
import matplotlib.pyplot as plt
from advent_of_code_helper.helper import read_lines_strip, fetch_data, fetch_test_data, int_str2list
from advent_of_code_helper.configuration import DDATA_YEAR


def convert_hand_to_count(hand_str):
    return [hand_str.count(i_str) for i_str in set(hand_str)]


def convert_count_to_rank(count_list):
    """
        Five of a kind, where all five cards have the same label: AAAAA
            --> count == 5
        Four of a kind, where four cards have the same label and one card has a different label: AA8AA
            --> count == 4 (this has len(2))
        Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
            --> count == 3 & count == 2 --> count == 3 and len(2)
        Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
            --> count == 3 & 2 * (count == 1) --> count == 3 and len(3)
        Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
            --> count ==  2 and count == 2 and count == 1 --> count(2) and len(3) (?)
        One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
            --> count ==  2 and count == 1 and count == 1 and count == 1 --> count(2) and len(4)
        High card, where all cards' labels are distinct: 23456
            --> len(5)

    """
    n_counts = len(count_list)
    max_count = max(count_list)
    if max_count == 5:
        return 6
    elif max_count == 4:
        return 5
    elif max_count == 3 and n_counts == 2:
        return 4
    elif max_count == 3 and n_counts == 3:
        return 3
    elif max_count == 2 and n_counts == 3:
        return 2
    elif max_count == 2 and n_counts == 4:
        return 1
    elif n_counts == 5:
        return 0
    else:
        print('uh-oh')


DAY = "7"
DDATA_DAY = os.path.join(DDATA_YEAR, DAY + '.txt')
DDATA_DAY_TEST = os.path.join(DDATA_YEAR, DAY + '_test.txt')

# Run get data..
_ = fetch_data(DAY)
_ = fetch_test_data(DAY)

# read input
puzzle_input = read_lines_strip(DDATA_DAY)
test_puzzle_input = read_lines_strip(DDATA_DAY_TEST)

selected_puzzle_input = puzzle_input

# This might help to order the labels
card_label2int = {k: ii + 1 for ii, k in enumerate("A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2".split(", ")[::-1])}

hand_type_bid = []
for i_line in selected_puzzle_input:
    hand_str, bid_int = i_line.split()
    bid_int = int(bid_int)
    hand_count = convert_hand_to_count(hand_str)
    hand_type = convert_count_to_rank(hand_count)
    hand_type_bid.append([hand_str, hand_type, bid_int])

resulting_sorting = sorted(hand_type_bid, key=lambda x: (x[1], ) +
                                                        ([card_label2int[x[0][i]] for i in range(len(x[0]))], ))

i_result = 0
for i_rank, (i_hand_str, _, i_bid) in enumerate(resulting_sorting):
    i_result += (i_rank+1) * i_bid

print(i_result)

"""
Update part 2
"""

card_label2int = {k: ii + 1 for ii, k in enumerate("A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J".split(", ")[::-1])}

hand_type_bid = []
for i_line in selected_puzzle_input:
    hand_str, bid_int = i_line.split()
    bid_int = int(bid_int)
    if 'J' in hand_str:
        n_J = hand_str.count('J')
        temp_hand_str = re.sub('J', '', hand_str)
        hand_count = convert_hand_to_count(temp_hand_str)
        hand_count = sorted(hand_count)
        if len(hand_count):
            hand_count[-1] += n_J
        else:
            hand_count = [n_J]
    else:
        hand_count = convert_hand_to_count(hand_str)

    hand_type = convert_count_to_rank(hand_count)
    hand_type_bid.append([hand_str, hand_type, bid_int])

resulting_sorting = sorted(hand_type_bid, key=lambda x: (x[1], card_label2int[x[0][0]], card_label2int[x[0][1]], card_label2int[x[0][2]], card_label2int[x[0][3]], card_label2int[x[0][4]]))

i_result = 0
for i_rank, (i_hand_str, _, i_bid) in enumerate(resulting_sorting):
    i_result += (i_rank+1) * i_bid

print(i_result)