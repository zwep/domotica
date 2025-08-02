import numpy as np
import os


"""

Helaas... heb nu niet mn dnig bij me

"""


def extract_return_text(file_path):
    with open(file_path, 'r') as f:
        A = f.readlines()

    A = [x.strip() for x in A]
    try:
        ind_start = A.index('Waar ga je werken?')
    except ValueError:
        ind_start = A.index('In welk werkveld kom je terecht?')
    try:
        ind_end = A.index('Wie ben jij?')
    except ValueError:
        ind_end = A.index('Wie ben je?')

    extracted_text = A[ind_start + 1:ind_end - 1]

    word_list = ' '.join(extracted_text).split(' ')
    if len(word_list) > 1:
        return word_list
    else:
        return []


def get_unique_files(file_list):
    stack = []
    filtered_list = []
    for i_file in file_list:
        file_split = i_file.split('_')
        base_name = file_split[0]
        num_ext = file_split[1]
        if base_name not in stack:
            stack.append(base_name)
            filtered_list.append(base_name + "_" + num_ext)
    return filtered_list


def get_capital_words(word_list):
    capital_words = []
    for ii, iword in enumerate(word_list):
        if len(iword):
            if iword[0].isupper():
                if word_list[max(0, ii - 1)].endswith('.'):
                    continue
                else:
                    capital_words.append(iword)
    return capital_words


def find_word_context(word, file_list):
    for ii, sel_file in enumerate(file_list):
        sel_file_path = os.path.join(dd, sel_file)
        word_list = extract_return_text(sel_file_path)
        for jj, sel_word in enumerate(word_list):
            if word in sel_word:
                print(sel_file)
                print(' '.join(word_list[max(jj-5, 0): min(len(word_list), jj + 5)]))
                return ii, jj


dd = '/media/bugger/MyBook/data/politie_vacancy'
file_list = os.listdir(dd)
unique_files = get_unique_files(file_list)

sel_file = unique_files[0]
all_capital_words = []
for sel_file in unique_files:
    sel_file_path = os.path.join(dd, sel_file)
    word_list = extract_return_text(sel_file_path)
    capital_words = get_capital_words(word_list)
    all_capital_words.extend(capital_words)

import collections
collections.Counter(all_capital_words)

# Based off the capital words I extracted.
# I would like to know where these words are...
selected_words = ['Kubernetes',
'OpenShift',
'CI/CD',
'RAPP',
'SBT',
'LMS systemen',
'Scrum Agile',
'PDC',
'LeSS',
'OSINT']

for sel_word in selected_words:
    print()
    _ = find_word_context(sel_word, unique_files)