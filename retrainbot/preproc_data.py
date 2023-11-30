import os
import collections
import re
import pathlib
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def get_base_name(file_name):
    base_name = pathlib.Path(file_name)
    for _ in base_name.suffixes:
        base_name = base_name.with_suffix('')

    return base_name.name


PREPROCESSING_DICT = {
    'WhatsApp Chat with Wocky! 353 Knuffels!': {'datetime': '%d/%m/%Y, %H:%M', 'date_length': 17},
    'WhatsApp Chat with Wocky! 27 keer nee': {'datetime': '%m/%d/%y, %H:%M', 'date_length': 14},
    "WhatsApp Chat_ _": {'datetime': '%d-%m-%y %H:%M:%S', 'date_length': 17},
    "WhatsApp Chat with Wocky! WhatSeb 🥜🥜🥜🥜🥜🥜": {'datetime': '%d/%m/%Y, %H:%M', 'date_length': 17},
    '_chat': {'datetime': '%d-%m-%y %H:%M:%S', 'date_length': 17},
    'celine_chat': {'datetime': '%d/%m/%Y, %H:%M:%S', 'date_length': 20},
}

"""

"""


def read_data(sel_file):
    path_file = os.path.join(DDATA, sel_file)

    with open(path_file, 'r') as f:
        raw_text_data = f.readlines()

    raw_text_data = [x.strip() for x in raw_text_data if len(x.strip())]
    return raw_text_data


def preprocess_datetime(raw_text_data, file_name):
    datetime_pattern = PREPROCESSING_DICT[file_name]['datetime']
    datetime_length = PREPROCESSING_DICT[file_name]['date_length']
    remove_string = '\ufeff|\u200e|(^\[)'
    wrong_lines = []
    correct_lines = []
    for sel_line in raw_text_data:
        sel_line = re.sub(remove_string, '', sel_line)
        date_substring = sel_line[:datetime_length].strip()
        message_substring = sel_line[datetime_length:].strip()
        try:
            date_obj = datetime.datetime.strptime(date_substring, datetime_pattern)
            correct_lines.append((date_obj, message_substring))
        except:
            wrong_lines.append(date_substring)

    print(f'Removed {int(len(wrong_lines) / len(raw_text_data) * 100)}% ({len(wrong_lines)} lines)')
    return correct_lines, wrong_lines


def preprocess_content(message_data, n_substring=2):
    """

    :param message_data:
    :param n_substring: Needed since each message now starts with '- ' or ': '
    :return:
    """
    filter_string = re.compile('Media omitted')
    filtered_message_data = [x[n_substring:] for x in message_data if not filter_string.findall(x)]
    n_orig = len(message_data)
    n_new = len(filtered_message_data)
    print(f'Removed {int((n_orig - n_new) / (n_orig) * 100)}% ({n_orig - n_new} lines)')
    return filtered_message_data


def preprocess_split_sender_message(message_data, spit_str=':'):
    """
    Each string is (I assume) composed of 'First name Last name: message'

    :param message_data:
    :param spit_str:
    :return:
    """
    post_message_list = []
    for x in message_data:
        x_split = x.split(spit_str)
        name = x_split[0]
        message = ' '.join(x_split[1:]).strip()
        post_message_list.append((name, message))
    return post_message_list


DDATA = '/home/bugger/Documents/data/wocky/seb_export'
list_files = os.listdir(DDATA)
sel_list_files = [x for x in list_files if 'celine' in x or 'Chat_ _' in x]

# Below we can contatenate ALL the data we have...
all_date_time_messages = []
for sel_file in sel_list_files:
    key_dict = get_base_name(sel_file)
    raw_text = read_data(sel_file)
    valid_date_time_message, wrong_lines = preprocess_datetime(raw_text, file_name=key_dict)
    all_date_time_messages.extend(valid_date_time_message)

# The preprocessing steps...
datetime_tuple, raw_message_tuple = zip(*all_date_time_messages)
message_list = preprocess_content(raw_message_tuple)
sender, message = zip(*preprocess_split_sender_message(message_list))

collections.Counter(sender)

datetime_tuple, message_list = zip(*all_date_time_messages)
datetime_hour_minute = []
for i_datetime in datetime_tuple:
    i_datetime = i_datetime.replace(year=2000, month=1, day=1)
    datetime_hour_minute.append(i_datetime)

"""
Plot activity over hours and years..
"""

# Plot of hours and minutes
fig, ax = plt.subplots()
_ = ax.hist(datetime_hour_minute, bins=1440)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.xaxis.set_minor_locator(mdates.HourLocator())
fig.suptitle('Verdeling van berichten over uren')

# Plot over months
fig, ax = plt.subplots()
_ = ax.hist([x.strftime('%b') for x in datetime_tuple], bins=12)
fig.suptitle('Verdeling van berichten over alle maanden')

# Plot over years
min_year = min(datetime_tuple, key=lambda x: x.year).year
max_year = max(datetime_tuple, key=lambda x: x.year).year
fig, ax = plt.subplots()
_ = ax.hist([x.year for x in datetime_tuple], bins=max_year - min_year)
fig.suptitle('Verdeling van berichten over alle jaren')


"""
Get the top-10 contributors to the Wocky whatsappp
"""

valid_message = preprocess_content(message_list)
post, message = zip(*preprocess_post(valid_message))
for k, v in collections.Counter(post).most_common(10):
    print(k, v)

"""
Nu kijken hoe lang mensen in de app zitten..
"""

top10_subjects = [k for k, v in collections.Counter(post).most_common(10)]
first_occurence = {}
for ii, i_message in enumerate(message_list):
    if len(top10_subjects) == 0:
        break
    else:
        found_someone = False
        n_subjects = len(top10_subjects)
        for i_subject in range(n_subjects):
            subject_name = top10_subjects[i_subject]
            if subject_name + ':' in i_message:
                found_someone = True
                break
        if found_someone:
            print(f'Found {subject_name} in {i_message}')
            top10_subjects.pop(i_subject)
            first_occurence[subject_name] = datetime_tuple[ii]

first_occurence
