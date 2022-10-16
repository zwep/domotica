
ddata = '/home/bugger/Documents/data/aoc/2021/input_day_12_test.txt'

with open(ddata, 'r') as f:
    list_of_entries = f.read().split('\n')

list_of_entries = [x for x in list_of_entries if x]


def flatten_list(x, temp=None):
    if temp is None:
        temp = []
    for i_x in x:
        if isinstance(i_x, list):
            flatten_list(i_x, temp)
        else:
            temp.append(i_x)
    return temp

list_of_entries = [x.split('-') for x in list_of_entries]
unique_entries = list(set(flatten_list(list_of_entries)))

visits = dict(zip(unique_entries, [0] * len(unique_entries)))
current_position = 'start'
next_position = None
for



