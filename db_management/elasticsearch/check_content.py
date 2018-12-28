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

con = es.Elasticsearch('192.168.1.7')

# Get "databases" .. or indices
res_indices = list(con.indices.get_alias('*').keys())

for i_ind in res_indices:
    print('Database: ', i_ind)
    temp = es_dsl.Search(using=con, index=i_ind)
    max_count = temp.count()
    print('Size: ', max_count)
