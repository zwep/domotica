# encoding: utf-8

import elasticsearch as es
import elasticsearch_dsl as es_dsl

import numpy as np
import pandas as pd

import sys
import os


if '__file__' in vars():
    project_path = os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir, os.path.pardir))
    print('\n Adding path: ', project_path)
    sys.path.append(project_path)

con = es.Elasticsearch('192.168.1.66')


# Get the source labels
# Get the counts per source labels
# Filter per source label..


# Get "databases" .. or indices
res_indices = list(con.indices.get_alias('*').keys())

for i_ind in res_indices:
    print('Database: ', i_ind)
    temp = es_dsl.Search(using=con, index=i_ind)

    temp.query('match')
    max_count = temp.count()
    print('Size: ', max_count)

sel_index = 'dutch_news'
# Get all the field names
res = con.search(index=sel_index, body={"query": {"match_all": {}}})
field_names = res['hits']['hits'][0]['_source'].keys()

# Wow, easy fix
# https://techoverflow.net/2019/03/17/how-to-fix-elasticsearch-fielddata-is-disabled-on-text-fields-by-default-for-keyword-field/
# Wat zijn keywords eigenlijk?

u_name = "unique_field"
for i_field in field_names:
    print(i_field)
    query_bod = {"aggs": {u_name: {"terms": {"size": 10, "field": "{}.keyword".format(i_field)}}}}
    res = con.search(index=sel_index, body=query_bod)
    field_bucket = res['aggregations'][u_name]['buckets']
    for i_bucket in field_bucket:
        print('\t\t', i_bucket['key'], i_bucket['doc_count'])

query_bod = {"query": { "match": {"category": "sporat"}}}
res = con.search(index='dutch_news', body=query_bod)
res.count()
res['aggregations'].keys()
[x['_source']['category'] for x in res['hits']['hits']]
temp[0]
temp.count()

# Multi-key aggregation]
query_bod = {"aggs": {"uniq_source": {"terms": {"field": "source.keyword"}, "aggs": {"uniq_cat": {"terms": {"field": "category.keyword"}}}}}}

res = con.search(index=sel_index, body=query_bod)
res_source = res['aggregations']['uniq_source']['buckets']
for i_source in res_source:
    print(i_source['key'])
    res_cat = i_source['uniq_cat']['buckets']
    for i_cat in res_cat:
        print('\t', i_cat['key'], i_cat['doc_count'])
field_bucket = res[u_name]
for i_bucket in field_bucket:
    print('\t\t', i_bucket['key'], i_bucket['doc_count'])