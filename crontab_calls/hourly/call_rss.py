# encoding: utf-8

"""
This is the script that can be run on a hourly basis in order to catch all the news items from various sources.
"""

from zwep.helper import loadrss as rss

import pytz
import os
from datetime import datetime
from pathlib import Path
from elasticsearch import Elasticsearch

es = Elasticsearch()
rss_obj = rss.RssUrl()
res_text = rss_obj.get_all_content()
news_source_list = rss_obj.news_source_list

update_file = 'last_update.txt'
update_path = '/var/log/domotica'
update_file_path = os.path.join(update_path, update_file)

if os.path.isfile(update_file_path):
    with open(update_file_path, 'r') as f:
        last_update = f.read()
else:
    # Just make some fake earlier date..
    last_update = '1999-12-31 01:01:01.01'
    # And create the file..
    with open(update_file_path, 'w') as f:
        f.write(last_update)



last_update = datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S.%f')
last_update = pytz.utc.localize(last_update)

new_items = 0
old_items = 0

for news_source in news_source_list:
    news_content = res_text[news_source]
    i_content = news_content[0]
    for i_content in news_content:
        content_date = datetime.strptime(i_content['date'], '%a, %d %b %Y %H:%M:%S %z')

        if content_date > last_update:
            new_items += 1
            es.index(index='dutch_news', body=i_content, doc_type='_doc')
        else:
            old_items += 1

    print('Seen {0} items'.format(new_items))
    print('Implemented {0} items'.format(old_items))


timezone_cor = pytz.timezone('Europe/Amsterdam')
current_time = str(datetime.now(timezone_cor))
with open(update_file_path, 'w') as f:
    f.write(current_time)
