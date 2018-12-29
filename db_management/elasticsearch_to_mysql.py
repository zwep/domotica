# encoding: utf-8

"""
Converserion of data from elasticsearch to mysql
"""


import elasticsearch as es
import elasticsearch_dsl as es_dsl
import sqlalchemy
import pymysql


import numpy as np
import pandas as pd
import pymysql

import os
import sys

if '__file__' in vars():
    project_path = os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir, os.path.pardir))
    print('\n Adding path: ', project_path)
    sys.path.append(project_path)

# Own code
from config import *

# Connection to Elasticsearch
con = es.Elasticsearch('localhost')
search_content = es_dsl.Search(using=con, index='netgear')
max_count = search_content.count()
res_content = search_content[0:max_count].execute()

# Content of netgear
res_filtered = [x['_source'].to_dict() for x in res_content['hits']['hits']]
A = pd.DataFrame.from_dict(res_filtered)


# Connection to MySQL
connection = pymysql.connect(host='localhost',
                             user=MYSQL_USER,
                             password=os.environ['seb_mysql_key'],
                             db=DB_NAME_NETGEAR)

cursor = connection.cursor()
cursor.execute('describe netgear')
B = cursor.fetchall()
col_names = [x[0] for x in B]

A_sel = A[col_names]

# Create engine
engine = sqlalchemy.create_engine('mysql+pymysql://{user}:{password}@localhost/{db}'.format(user=MYSQL_USER,
                                                                                    password=os.environ['seb_mysql_key'],
                                                                                    db=DB_NAME_NETGEAR))

# Add data to the database
A_sel.to_sql(TABLE_NAME_NETGEAR, con=engine, index=False, if_exists='append')