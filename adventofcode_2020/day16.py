import numpy as np
day = 16
with open(f"adventofcode_2020/day{str(day)}_numbers.txt", "r") as f:
    A = f.readlines()


A_split = ''.join([x if x != '\n' else '***' for x in A]).split('***')
A_ranges = A_split[0].split('\n')[:-1]
A_ticket = A_split[1].split('\n')
A_nearby_ticket = A_split[2].split('\n')[1:-1]

# range extractor
i_line = A_ranges[0]

def range_extractor(i_line):
    print(i_line)
    range_1, range_2 = i_line.split(":")[1].strip().split(" or ")
    numbers = []

    for i_range in [range_1, range_2]:
        t0, t1 = i_range.split('-')
        numbers.extend(list(range(int(t0), int(t1)+1)))
    return numbers

A_number_range = [range_extractor(x) for x in A_ranges]

faulty_numbers = []
for i, i_ticket in enumerate(A_nearby_ticket):
    ticket_int = [int(x) for x in i_ticket.split(",")]
    result_ticket = []
    for i_number in ticket_int:
        result_ticket.append([i_number in x for x in A_number_range])
    res = np.sum(np.array(result_ticket), axis=1)
    if len(np.argwhere(res == 0)):
        faulty = np.array(ticket_int)[np.argwhere(res==0)[0]]
        faulty_numbers.append((i, int(faulty)))

sum([x[1] for x in faulty_numbers])

# Part 2
faulty_tickets = [x[0] for x in faulty_numbers]
A_filtered_tickets = [x for i, x in enumerate(A_nearby_ticket) if i not in faulty_tickets]

all_ticket_check = []
for i, i_ticket in enumerate(A_filtered_tickets):
    print(i_ticket)
    ticket_int = [int(x) for x in i_ticket.split(",")]
    result_ticket = []
    for i_number in ticket_int:
        result_ticket.append([i_number in x for x in A_number_range])

    all_ticket_check.append(result_ticket)


everything_combined = np.array(all_ticket_check)
A_prod = np.prod(everything_combined, axis=0)
for i in range(1, 21):
    print(np.argwhere(np.prod(everything_combined, axis=0).sum(axis=0)==i) + 1)

A_prod = np.prod(everything_combined, axis=0)
index_left = np.array(list(range(0, 20)))
while (A_prod == -1).sum() != 400:
    # print(A_prod[index_left], end='\n\n')
    for j_col in range(20):
        # sel_col = A_prod[index_left, j_col] == 1
        sel_col = A_prod[:, j_col] == 1
        zsum = sum(sel_col)
        if zsum == 1:
            print(np.argwhere(sel_col), j_col)
            # index_left[int(np.argwhere(sel_col))] = -1
            A_prod[int(np.argwhere(sel_col)), :] = -1
            A_prod[:, j_col] = -1
            # index_left = np.array([x for x in index_left if x !=-1])
            break
#
my_ticket = [int(x) for x in A_ticket[1].split(",")]
my_ticket[11] * my_ticket[14] * my_ticket[2] * my_ticket[4] * my_ticket[7] * my_ticket[16]