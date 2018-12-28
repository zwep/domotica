# encoding: utf-8

"""

"""

import config
import MySQLdb
import os
import db_management.mysql.check_content as check_mysql
from netgear_code.get_netgear import get_netgear_devices
import sqlalchemy


seb_mysql_key = os.environ['seb_mysql_key']
db_name = 'domotica'
table_name = 'netgear_code'
db_user = 'seb'

# Obtaining netgear_code devices
A = get_netgear_devices()


# Create database...
con = MySQLdb.connect('localhost', 'seb', seb_mysql_key)
cursor = con.cursor()

print('Creating database: ', db_name)
cursor.execute("CREATE DATABASE IF NOT EXISTS {0}".format(db_name))
res = check_mysql.check_database_name(cursor, db_name)


# Create engine
engine = sqlalchemy.create_engine('mysql://{user}:{password}@localhost/{db}'.format(user=db_user,
                                                                                    password=seb_mysql_key,
                                                                                    db=db_name))

# Add data to the database
A.to_sql('netgear_code', con=engine, index=False)

# Empty the content of the database - so we are only left with the schema
cursor.execute("USE {db_name}".format(db_name=db_name))
cursor.execute("TRUNCATE TABLE {table_name}".format(table_name=table_name))
check_mysql.check_table_name(cursor, table_name, db_name)

# Check content
cursor.execute("SELECT * FROM {table_name};".format(table_name=table_name))
B = cursor.fetchall()

print('Content of table: {table_name}'.format(table_name=table_name))
for x in B:
    print(x)
