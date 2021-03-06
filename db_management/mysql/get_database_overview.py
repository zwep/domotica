# encoding: utf-8


import pymysql
import os
import sys

if '__file__' in vars():
    project_path = os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir, os.path.pardir))
    print('\n Adding path: ', project_path)
    sys.path.append(project_path)

# Own code
from config import *
import db_management.mysql.check_content as check_content


seb_mysql_key = os.environ['seb_mysql_key']
conn = pymysql.connect('192.168.1.5:3306', 'seb', seb_mysql_key)
import MySQLdb
MySQLdb.connect('192.168.1.5:3306', 'seb', seb_mysql_key)
cursor = conn.cursor()

# Show databases
databases = "show databases"
cursor.execute(databases)
res_databases = [x[0] for x in cursor.fetchall()]
filter_databases = [x for x in res_databases if x not in DATABASE_FILTER]

print('\n Overview databases \n')
for i in res_databases:
    print('\t ', i)

print('\n Overview tables in databases \n')
# Show tables
for i_db in res_databases:
    cursor.execute("use " + i_db)
    cursor.execute("show tables")
    res_tables = cursor.fetchall()
    print('\t Database: ', i_db)
    if len(res_tables):
        for i_table in res_tables:
            print('\t\t Table name: ', i_table[0])
            if i_db in filter_databases:
                check_content.check_table_content(cursor, i_table[0], i_db)
    else:
        print('\t\t No tables have been found')
