# encoding: utf-8

"""
This is the script that can be run on a hourly basis in order to catch all the news items from various sources.
"""

from RSS import news_rss as rss
import pytz
import os
from datetime import datetime
from dateutil.parser import parse as duparse
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
    last_update = '1999-12-31 01:01:01.01+02:00'
    # And create the file..
    with open(update_file_path, 'w') as f:
        f.write(last_update)

# With this we parse the date that was found in the file
last_update = duparse(last_update)

# Here we loop over all the news sources and add all the items to ElasticSearch
# But only if their publication date is after our latest update
for news_source in news_source_list:
    # Keep track of items per news source
    new_items = 0
    old_items = 0

    news_content = res_text[news_source]
    i_content = news_content[0]
    for i_content in news_content:
        content_date = duparse(i_content['date'])

        if content_date > last_update:
            # A check to see if our date comparisson is correct
            n_space = ' '*(len(str(content_date))-len('Content') + 1)
            print('Content' + n_space + 'Last update')
            print(content_date, last_update)

            new_items += 1
            es.index(index='dutch_news', body=i_content, doc_type='_doc')
        else:
            old_items += 1

    # Overview of the implemented and seen items
    print('News soure: ', news_source)
    print('Old {0} items'.format(old_items))
    print('New {0} items'.format(new_items))
    print('---------------\n')


timezone_cor = pytz.timezone('Europe/Amsterdam')
current_time = str(datetime.now(timezone_cor))
with open(update_file_path, 'w') as f:
    f.write(current_time)
