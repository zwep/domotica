# Alternative to one...
import re
with open("adventofcode_2020/day6_numbers.txt", "r") as f:
    A = f.read().splitlines()


string_dicts = ''.join([x if x != '' else '***' for x in A]).split('***')
s0 = 0
for i_group in string_dicts:
    s0 += len(set(i_group))

print(s0)

# Dag 2
string_dicts = ' '.join([x if x != '' else '***' for x in A]).split('***')
s0 = 0
for i_group in string_dicts:
    temp_list = [set(x) for x in i_group.strip().split()]
    s0 += len(set.intersection(*temp_list))

print(s0)