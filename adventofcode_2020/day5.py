
# Alternative to one...
import re
with open("adventofcode_2020/day5_numbers.txt", "r") as f:
    A = f.read().splitlines()


def get_pos(min_row, max_row, i_line):
    counter = 0
    while counter < len(i_line):
        if i_line[counter] == "F" or i_line[counter] == "L":
            max_row = (max_row - min_row) // 2 + min_row
        elif i_line[counter] == "B" or i_line[counter] == "R":
            min_row = (max_row - min_row) // 2 + min_row

        # print(i_line[counter], min_row, max_row, counter)
        counter += 1
    return min_row, max_row


max_row = 128
min_row = 0
max_col = 8
max_value = 0
id_list = []
for i_line in A:
    row = get_pos(min_row, max_row, i_line[:-3])[0]
    col = get_pos(0, max_col, i_line[-3:])[0]
    max_id = row * 8 + col
    id_list.append(max_id)

print(max(id_list))

id_list = sorted(id_list)
id_list[544]
id_list[545]
[x - y for x, y in zip(id_list[1:], id_list[:-1])].index(2)
get_pos(0, 128, "FFFFFFF")[0] * 8 + get_pos(0, 8, "RRR")[0]