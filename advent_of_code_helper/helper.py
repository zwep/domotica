import os
import requests
from bs4 import BeautifulSoup
import re
from advent_of_code_helper.configuration import YEAR, DDATA_YEAR


class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def read_lines(file_path):
    with open(file_path, 'r') as f:
        content = f.readlines()
    return content


def read_lines_strip(file_path):
    with open(file_path, 'r') as f:
        content = f.readlines()

    return [x.strip('\n') for x in content]


def fetch_data(day):
    """
    Function to get YOUR puzzle input from the html page

    :param day: which day is it...
    :return:
    """
    ddata_day = os.path.join(DDATA_YEAR, day + '.txt')
    if os.path.isfile(ddata_day):
        return -1
    else:
        fetch_data = f"aocdl -day {day} -year {YEAR} -output {ddata_day}"
        os.system(fetch_data)
        return 1


def fetch_test_data(day):
    """
    Function to get the test puzzle input from the html page

    :param day: which day is it...
    :return:
    """
    ddata_day = os.path.join(DDATA_YEAR, day + '_test.txt')
    if os.path.isfile(ddata_day):
        return -1
    else:
        re_example = re.compile(r'example.*:', re.I)
        url = f'https://adventofcode.com/{YEAR}/day/{day}'
        # Send an HTTP request to the URL and get the HTML content
        response = requests.get(url)
        html_content = response.text
        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # Loop through all the <p> things
        preamble_example_obj = None
        for i_p in soup.find_all('p'):
            if re_example.findall(i_p.text):
                # Stop when we find the first.
                preamble_example_obj = i_p
                break
        # Extract the <code> block after the word 'example'
        code_block = preamble_example_obj.find_next('pre').find('code')
        # Dont use any formatter, default formatter messes up some special chars like >
        test_puzzle_input = code_block.prettify(formatter=None)
        test_puzzle_input = re.sub('</code>|<code>', '', test_puzzle_input).strip()
        # Store input
        with open(ddata_day, 'w') as f:
            f.write(test_puzzle_input)


def int_str2list(int_str, sep=None):
    # Convert "1 3 4" to [1,3,4]
    # Convert "1,3,4" to [1,3,4] when sep = ','
    return list(map(int, int_str.split(sep)))


def get_column(input_list, col_index, to_str=False):
    if to_str:
        return ''.join([i_line[col_index] for i_line in input_list])
    else:
        return [i_line[col_index] for i_line in input_list]


def transpose_of_nested_list(input_list, to_str=False):
    # Puzzle input is often ['234', '252', ..., '235']
    transposed_list = []
    n_col = len(input_list[0])
    for ii in range(n_col):
        temp = get_column(input_list, ii)
        if to_str:
            transposed_list.append(''.join(temp))
        else:
            transposed_list.append(temp)
    return transposed_list


def difference_element_list(input_list):
    return [j-i for i, j in zip(input_list[:-1], input_list[1:])]