# encoding: utf-8

import os
import MySQLdb
import config

seb_mysql_key = os.environ['seb_mysql_key']
conn = MySQLdb.connect('localhost', 'seb', seb_mysql_key)
cursor = conn.cursor()

# Show databases
databases = ("show databases")
cursor.execute(databases)
res_databases = cursor.fetchall()

print('\n Overview databases \n')
for i in res_databases:
    print('\t ', i)

print('\n Overview tables in databases \n')
# Show tables
for i_db in res_databases:
    cursor.execute("use " + i_db[0])
    cursor.execute("show tables")
    res_tables = cursor.fetchall()
    print('\t Database: ', i_db)
    if len(res_tables):
        for i_table in res_tables:
            print('\t\tTable name: ', i_table)
    else:
        print('\t\t No tables have been found')
        