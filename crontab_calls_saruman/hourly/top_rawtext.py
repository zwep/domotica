# encoding: utf-8

"""
This program should be run right after we have obtained a snapshot of nvidia-smi

So in the same bash program we will write something like...
Oooor we can run this daily... that is also a nice idea. Reducing the amount of calls by... 24!

python(3) nvidia_rawtext.py -i <name of the file we just created>

lol ik weet ff niet meer hoe de data wordt opgeslagen...
VOlgens mij alles in 1 file... die wordt geappend...

Eh we zien wel. Dit ding werkt sowieso wel
"""

import re
import pandas as pd
import argparse
import os

arg_parse = argparse.ArgumentParser()
arg_parse.add_argument('-i', help='Gives the input path name to process', type=str)
parsed_arg = arg_parse.parse_args()


def parse_raw_to_csv(input_file):
    """
    Here we are going ato parse the input raw_text file to a csv.. which we can later use to plot stuff with
    :param input_file: Full path to a rawfile from nvidia
    :return:
    """
    assert input_file, "Please specify an input file with -i"

    with open(input_file, 'r') as f:
        a_text = f.read()

    # input_file = '/home/charmmaria/data/top_rawtext/2018_10_18_rawfile.txt'
    # input_file = i_file
    # input_file = list_files[0]
    raw_date = re.findall("([0-9]{4}_[0-9]{2}_[0-9]{2})_rawfile.txt", input_file)
    # print(raw_date)
    parsed_text = [x.split('\n') for x in a_text.split('TIMESTAMP: ')]
    # Select columns if there is PID in any of the elements...
    sel_text = [x for x in parsed_text if 'PID' in ''.join(x)]
    # Then use one selected piece of text to extract the column names
    example_output = [x for x in sel_text if 'PID' in ''.join(x)][0]
    str_colname = example_output[1].split()
    hourly_data = []

    for i_text_stamp in parsed_text:
        i_timestamp = i_text_stamp[0]
        i_datestamp = raw_date[0] + ' ' + i_timestamp
        raw_str_values = [x for x in i_text_stamp[1:] if '%' not in x]
        str_values = [[i_datestamp] + x.split() for x in raw_str_values]
        hourly_data.extend(str_values)

    hourly_data = [x for x in hourly_data if len(x) > 1]

    # We need to ditch the last one like this.. because it has a space we can fix easily.
    col_names = ['Time'] + str_colname
    n_col = len(col_names)
    hourly_data = [x if len(x) == n_col else x[:(n_col-1)] + [' '.join(x[n_col:])] for x in hourly_data]

    return col_names, hourly_data


if __name__ == '__main__':
    if parsed_arg.i:
        path_to_text = parsed_arg.i
    else:
        path_to_text = ''
        path_to_text = '/home/bugger/Documents/data/top'

    daily_data = []
    list_files = [os.path.join(path_to_text, x) for x in os.listdir(path_to_text) if x.endswith('rawfile.txt')]
    list_files = sorted(list_files)

    for i_file in list_files:
        col_names, hourly_data = parse_raw_to_csv(i_file)
        daily_data.extend(hourly_data)

    # This is not workin as pretty... if we had a numpy thing that could convert it to csv, then it would ve really great.
    # col_names.extend(overview_data)
    # import numpy as np
    # np.array(col_names).tofile('/home/charmmaria/test_csv.csv')

    csv_filename = os.path.join(path_to_text, 'top_database.csv')
    A = pd.DataFrame(daily_data)
    A.columns = col_names
    A.to_csv(csv_filename, index=False, sep='#')
