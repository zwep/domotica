# encoding: utf-8

"""
Here we show the status of ElasticSearch with respect to news
data. Just to see how many duplicates we generate and where..
"""

import zwep.helper.elasticsearch as es_help

all_content = es_help.get_all_content()
dupli_dict = es_help.identify_duplicate_titles(all_content)
dupli_content = es_help.find_duplicate_titles(dupli_dict)


