# encoding: utf-8

"""
This program should be run right after we have obtained a snapshot of nvidia-smi

So in the same bash program we will write something like...
Oooor we can run this daily... that is also a nice idea. Reducing the amount of calls by... 24!

python(3) nvidia_rawtext.py -i <path to directory of all the nvidia-smi files.>

In the same directory, we will store the 'database'
"""

import re
import pandas as pd
import argparse
import os
import sys

if os.name == 'nt':
    windows_system = True
else:
    windows_system = False


arg_parse = argparse.ArgumentParser()
arg_parse.add_argument('-i', help='Gives the input path name to process', type=str)
# This is to prevent some malfunctioning of argpars when we run it in console
sys.argv = ['test3.py', '-i', '']
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

    # input_file = '/home/bugger/Documents/data/nvidia_saruman/2018_10_18_rawfile.txt'

    raw_date = re.findall("([0-9]{4}_[0-9]{2}_[0-9]{2})_rawfile.txt", input_file)
    # print(raw_date)
    parsed_text = [x.split('\n') for x in a_text.split('TIMESTAMP: ')]

    # Get all the hourly data from the parsed text
    hourly_data = []
    for i_text_stamp in parsed_text:
        i_timestamp = i_text_stamp[0]
        i_datestamp = raw_date[0] + ' ' + i_timestamp

        raw_str_values = [x for x in i_text_stamp[1:] if '%' in x]
        str_values = [[i_datestamp, str(i_gpu).zfill(2)] +
                      re.sub(' / ', '/', re.sub('\|', '', x)).split() for i_gpu, x in enumerate(raw_str_values)]
        # If something goes wrong.. use these values..
        # Only do this when we couldnt find anything BUT we did have a timestamp.
        if len(str_values) == 0 and i_timestamp:
            default_str_values = ['-10%', '-10C', 'P8', '-10W/100W', '-10MiB/100MiB', '-10%', 'Default']
            str_values = [[i_datestamp, str(i_gpu).zfill(2)] + default_str_values for i_gpu in range(8)]
        # Aggregate all the information into this list of lists..
        hourly_data.extend(str_values)

    # Extract a representative piece of text that contains raw text from nvidia-smi
    # Make sure to avoid error messages, or empty messages. This is done by demanding a certain length (now 30)
    sel_text = [x for x in parsed_text if len(x) > 25]
    if sel_text:
        sel_text = sel_text[0]

        # Use one selected piece of text to extract the column names. We know that if the name 'Fan' is in there,
        # the other column names will be there as well
        str_colname = [x for x in sel_text if 'Fan' in x][0]
        # We need to ditch the last one like this.. because it has a space we can fix easily.
        col_names = [['Time', 'GPU'] + re.sub(' / ', '/', re.sub('\|', '', str_colname)).split()[:-1]]
    else:
        col_names = None
        hourly_data = []

    return col_names, hourly_data


if __name__ == '__main__':
    if parsed_arg.i:
        path_to_text = parsed_arg.i
    else:
        if windows_system:
            path_to_text = r'C:\Users\20184098\Documents\data\nvidia'
        else:
            # path_to_text = '/home/charmmaria/data/nvidia'
            # path_to_text = '/home/charmmaria/data/nvidia'
            # path_to_text = '/home/bugger/Documents/data/nvidia'
            path_to_text = '/home/bugger/Documents/data/nvidia_saruman'

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

    csv_filename = os.path.join(path_to_text, 'nvidia_database.csv')
    A = pd.DataFrame(daily_data)
    A.columns = col_names
    A.to_csv(csv_filename, index=False)
