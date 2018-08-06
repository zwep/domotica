# encoding: utf-8

"""
How to store the text data? Elastic DB?


TODO test this thing
TODO upload it to git..

Layout of the folder/table structure

/data
    /text
        /news (or social media..)
            /nos
                /date (YYYY-MM-DD)
                    /morning
                    /noon
                    /afternoon
            /...
"""

from zwep.helper import loadrss as rss

import os
import time
from pathlib import Path


def create_path(path):
    """
    With this we want to check the directory..
    :param path:
    :return:
    """
    if not os.path.isdir(path):
        Path(path).mkdir(parents=True, exist_ok=True)
        print('\n Created path: ', path)
    else:
        print('\n Path already exists: ', path)


def check_duplicate(orig_data, new_data):
    """
    Here we will chekc if we already have the relveant info..
    :param orig:
    :param new:
    :return:
    """
    # maybe sort the new data
    title_text = [x['title'] for x in new_data]
    orig_title_text = [x['title'] for x in orig_data]

    for i, i_title in enumerate(title_text):
        if i_title in orig_title_text:
            print(i)


PATH_TEXT_DATA = '/home/data/text'
PATH_SPEC = os.path.join(PATH_TEXT_DATA, 'news')

A = rss.RssUrl()
res_text = A.get_all_content()
news_source_list = A.news_source_list

t_time = time.localtime()
t_date = [str(t_time.tm_year), str(t_time.tm_mon).zfill(2), str(t_time.tm_mday).zfill(2)]
t_hour = t_time.tm_hour

if t_hour > 0 and t_hour < 12:
    t_hour_class = 'morning'
elif t_hour >= 12 and t_hour < 18:
    t_hour_class = 'noon'
elif t_hour >= 18 and t_hour < 24:
    t_hour_class = 'evening'
else:
    print('Something went wrong')
    t_hour_class = 'unkown'

news_path_list = {x: os.path.join(PATH_SPEC, x, '/'.join(t_date)) for x in news_source_list}

for news_source, news_path in news_path_list.items():
    create_path(news_path)
    news_source = 'nos'
    res_text[news_source].keys()