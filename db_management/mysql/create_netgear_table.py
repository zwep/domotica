# encoding: utf-8

"""

"""

import config
from netgear.get_netgear import get_netgear_devices
import MySQLdb
import os
from db_management.mysql.check_content import check_database_name

seb_mysql_key = os.environ['seb_mysql_key']
con = MySQLdb.connect('localhost', 'seb', seb_mysql_key)
cursor = con.cursor()


db_name = 'domotica'
table_name = 'netgear'
A = get_netgear_devices()
column_name = A.columns

# Create database...
res = check_database_name(cursor, db_name)

if not res:
    print('Creating database: ', db_name)
    cursor.execute("CREATE DATABASE " + db_name)

res = check_database_name(cursor, db_name)
if res:
    print('Succesfully created database')
else:
    print('Database not created.')

# Create table
