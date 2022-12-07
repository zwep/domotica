import os
import re
from adventofcode_2022.helper import DPATH


class FileDirectory:
    def __init__(self, parent, name, folder, file_size):
        self.parent = parent
        self.name = name
        self.file_size = file_size
        self.sub_folder_list = folder

    def sum(self):
        return sum(self.file_size + [x.sum() for x in self.sub_folder_list])

    def print(self, depth=0):
        print('  ' * depth, self.name, self.sum())
        [x.print(depth=depth+1) for x in self.sub_folder_list]

    def get_sum_directories(self, temp_dict=None):
        if temp_dict is None:
            temp_dict = {}
        else:
            temp_dict[self.name] = self.sum()
            return [x.get_sum_directories(temp_dict=temp_dict) for x in self.sub_folder_list]

        return temp_dict

    def find_subfolder(self, name):
        for x in self.sub_folder_list:
            if x.name == name:
                return x

    def get_root(self):
        if self.parent is None:
            return self
        else:
            return self.parent.get_root()


def find_next_command(sample_puzzle_input):
    for i, x in enumerate(sample_puzzle_input):
        if x.startswith('$'):
            return i
    return None


def split_file_directory(string_list):
    dir_name_list = [get_dir_name.findall(x)[0] for x in string_list if x.startswith('dir')]
    file_size_list = [int(re.findall('([0-9]+)', x)[0]) for x in string_list if not x.startswith('dir')]
    return dir_name_list, file_size_list


def get_nested_sum(object, state):
    state.append(object.sum())
    if len(object.sub_folder_list):
        for i_sub_object in object.sub_folder_list:
            get_nested_sum(i_sub_object, state)
    return state


def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])


dfile = os.path.join(DPATH, 'day7.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x.strip() for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if len(x)]

sample_input = puzzle_input

get_cd_name = re.compile('cd (\w+|/)')
get_dir_name = re.compile('dir (\w+)')

current_directory_obj = None
i_index = 0
while i_index < len(sample_input):
    input_line = sample_input[i_index]
    i_next = 0
    if input_line.startswith('$ cd ..'):
        current_directory_obj = current_directory_obj.parent
    elif input_line.startswith('$ cd'):
        directory_name = get_cd_name.findall(input_line)[0]
        if current_directory_obj is None:
            # Create the parent directory
            current_directory_obj = FileDirectory(file_size=[], folder=[], name=directory_name, parent=current_directory_obj)
        else:
            # Find the child directory
            current_directory_obj = current_directory_obj.find_subfolder(directory_name)
    elif input_line.startswith('$ ls'):
        i_next = find_next_command(sample_input[(i_index+1):])
        if i_next is None:
            i_next = len(sample_input)
        list_of_file_dir = sample_input[i_index+1:i_index + i_next + 1]
        dir_name, file_sizes = split_file_directory(list_of_file_dir)
        dir_name_objects = [FileDirectory(file_size=[], folder=[], name=x, parent=current_directory_obj) for x in dir_name]
        # Check if previous command was cd 'directory'?
        current_directory_obj.file_size.extend(file_sizes)
        current_directory_obj.sub_folder_list.extend(dir_name_objects)
    else:
        print('Unknown command ', input_line)

    i_index += i_next + 1

main_obj = current_directory_obj.get_root()
_ = main_obj.print()

res = get_nested_sum(main_obj, [])
sum([v for v in res if v < 100000])

# Part 2
currently_used = main_obj.sum()
total_disk_space = 70000000
required_unused_space = 30000000
currently_unused = total_disk_space - currently_used
amount_to_delete = required_unused_space - currently_unused
possible_sizes_to_delete = [x for x in res if x >= amount_to_delete]
min(possible_sizes_to_delete)



# sum([v for k, v in res.items() if v <= 100000])
#
#
# len([get_cd_name.findall(x)[0] for x in puzzle_input if get_cd_name.findall(x)])
# import collections
# collections.Counter([get_cd_name.findall(x)[0] for x in puzzle_input if get_cd_name.findall(x)]).most_common(10)
# len(set([get_cd_name.findall(x)[0] for x in puzzle_input if get_cd_name.findall(x)]))
#
# all_directories = set([get_cd_name.findall(x)[0] for x in puzzle_input if get_cd_name.findall(x)])
# all_directories.difference(set(res.keys()))
#
