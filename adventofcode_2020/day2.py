

with open("adventofcode_2020/day2_numbers.txt", "r") as f:
    A = f.readlines()

counter_pass = 0
for i_line in A:
    cond, password = i_line.split(":")
    count, letter = cond.split()
    min, max = count.split("-")
    if int(min) <= password.count(letter) <= int(max):
        counter_pass += 1


# Part 2
counter_pass = 0
for i_line in A:
    cond, password = i_line.split(":")
    password = password.strip()
    count, letter = cond.split()
    min, max = count.split("-")
    min = int(min)
    max = int(max)

    if (password[min - 1] == letter) != (password[max - 1] == letter):
        counter_pass += 1