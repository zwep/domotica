
day = 14
with open(f"adventofcode_2020/day{str(day)}_numbers.txt", "r") as f:
    A = f.read().splitlines()

mem = [0]

#
# binary_string_to...
# for i_line in A:

name, value_mask = A[0].split('=')
value_mask = value_mask.strip()
n_mask = len(value_mask)
binary_mask = [(i, x) for i, x in enumerate(value_mask[::-1]) if x!='X']

name, value = A[1].split('=')
str(bin(int(value)))[2:]
current_value = list(format(int(value), f"#0{n_mask}b"))
for i_index, new_value in binary_mask:
    current_value[i_index+2] = new_value
    ''.join(current_value)
