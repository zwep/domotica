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

import os
import re
import pandas as pd
import argparse

arg_parse = argparse.ArgumentParser()
arg_parse.add_argument('-i', help='Gives the input path name to process', type=str)
parsed_arg = arg_parse.parse_args()

if parsed_arg.i:
    path_to_text = '/home/charmmaria/data/nvidia_rawtext'
    # Use an arg parse...
    i_file = os.listdir(path_to_text)[0]

def parse_raw_to_csv(input_path):
    """
    Here we are going ato parse the input raw_text file to a csv.. which we can later use to plot stuff with
    :param input_file: Full path to a rawfile from nvidia
    :return:
    """
    list_files = [x for x in os.listdir(input_path) if x.endswith('rawtext.txt')]

    daily_data = []

    for input_file in list_files:
        with open(input_file, 'r') as f:
            a_text = f.read()

        parsed_text = [x.split('\n') for x in a_text.split('TIMESTAMP: ')]
        sel_text = parsed_text[1]
        hourly_data = []

        for i_text_stamp in parsed_text:
            i_timestamp = i_text_stamp[0]
            raw_str_values = [x for x in i_text_stamp[1:] if '%' in x]
            str_values = [[i_timestamp, str(i_gpu).zfill(2)] +
                          re.sub(' / ', '/', re.sub('\|', '', x)).split() for i_gpu, x in enumerate(raw_str_values)]
            hourly_data.extend(str_values)


    # Use one selected piece of text to extract the column names
    str_colname = [x for x in sel_text if 'Fan' in x][0]
    # We need to ditch the last one like this.. because it has a space we can fix easily.
    col_names = [['Time', 'GPU'] + re.sub(' / ', '/', re.sub('\|', '', str_colname)).split()[:-1]]

    # This is not workin as pretty... if we had a numpy thing that could convert it to csv, then it would ve really great.
    # col_names.extend(overview_data)
    # import numpy as np
    # np.array(col_names).tofile('/home/charmmaria/test_csv.csv')

    csv_filename = re.sub('rawfile\.txt', 'csvfile.csv', i_file)
    A = pd.DataFrame(overview_data)
    A.columns = col_names
    A.to_csv(csv_filename, index=False)
