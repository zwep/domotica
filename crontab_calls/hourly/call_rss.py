# encoding: utf-8

"""
How to store the text data? Elastic DB?


TODO test this thing
TODO upload it to git..
"""

from zwep.helper import loadrss as rss
from config import *
import os
import time


PATH_SPEC = os.path.join(PATH_TEXT_DATA, 'news')

A = rss.Rssurl()
res_text = A.get_url_content()

t_time = time.localtime()
if t_time.tm_hour > 0 and t_time.tm_hour < 12:
    t_hour_class = 'morning'
elif t_time.tm_hour >= 12 and t_time.tm_hour < 18:
    t_hour_class = 'noon'
elif t_time.tm_hour >= 18 and t_time.tm_hour < 24:
    t_hour_class = 'evening'
else:
    print('Something went wrong')
    t_hour_class = 'unkown'

date_str = str(t_time.tm_year) + str(t_time.tm_month) + str(t_time.tm_day) + t_hour_class

for i_key, i_value in res_text.items():
    PATH_SOURCE = os.path.join(PATH_SPEC, i_key)
    # Make sure that we have a path to the news source..
    if not os.path.isdir(PATH_SOURCE):
        os.makedirs(PATH_SOURCE)

    for i_label, i_content in i_value.items():
        # Now do some saving of the text.. or some preprocessing.
        PATH_LABEL = os.path.join(PATH_SOURCE, i_label)
        if not os.path.isdir(PATH_LABEL):
            os.makedirs(PATH_LABEL)
        file_name = date_str + 'text.txt'
        with open(file_name, 'w') as f:
            f.write(i_content)

