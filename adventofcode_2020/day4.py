
# Alternative to one...
import re
with open("adventofcode_2020/day4_numbers.txt", "r") as f:
    A = f.read().splitlines()

string_dicts = ','.join([re.sub(' ', ',', x) if x != '' else '***' for x in A]).split('***')
list_key = []
for x in string_dicts:
    print('\n\n')
    temp_key = []
    if x.endswith(","):
        x = x[:-1]
    if x.startswith(","):
        x = x[1:]
    for y in x.split(","):
        key, value = y.split(":")
        if key != 'cid':
            temp_key.append(key)
    list_key.append(temp_key)


sum([len(x) == 7 for x in list_key])

"""

    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.

"""

# Alternative to one...
import re
with open("adventofcode_2020/day4_numbers.txt", "r") as f:
    A = f.read().splitlines()

string_dicts = ','.join([re.sub(' ', ',', x) if x != '' else '***' for x in A]).split('***')
list_key = []
for x in string_dicts:
    print('\n\n')
    temp_key = []
    if x.endswith(","):
        x = x[:-1]
    if x.startswith(","):
        x = x[1:]

    for y in x.split(","):
        key, value = y.split(":")
        print(key, value)
        if key == "byr":
            if 1920 <= int(value) <= 2002:
                print('\t\tbyr pass')
                temp_key.append(True)
        if key == 'iyr':
            if 2010 <= int(value) <= 2020:
                print('\t\tiyr pass')
                temp_key.append(True)
        if key == 'eyr':
            if 2020 <= int(value) <= 2030:
                print('\t\teyr pass')
                temp_key.append(True)
        if key == "hgt":
            #If cm, the number must be at least 150 and at most 193.
            #If in, the number must be at least 59 and at most 76.
            if value.endswith('cm'):
                if 150 <= int(value[:-2]) <= 193:
                    print('\t\thgt pass')
                    temp_key.append(True)
            if value.endswith('in'):
                if 59 <= int(value[:-2]) <= 76:
                    print('\t\thgt pass')
                    temp_key.append(True)
        if key == 'hcl':
            value_match = re.match('#([0-9a-f]{6})', value)
            if value_match is not None:
                print('\t\thcl pass')
                temp_key.append(True)
        # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
        if key == 'ecl':
            if value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]:
                print('\t\tecl pass')
                temp_key.append(True)
        if key == 'pid':
            if len(value) == 9:
                print('\t\tpid pass')
                temp_key.append(True)
        # if key != 'cid':
        #     # DO some vlaue stuff...
        #     temp_key.append(key)


    list_key.append(temp_key)


sum([len(x)==7 for x in list_key])
