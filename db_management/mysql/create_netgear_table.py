# encoding: utf-8

"""

"""

import sys
import pymysql
import os
import sqlalchemy

if '__file__' in vars():
    project_path = os.path.abspath(os.path.join(__file__, os.path.pardir, os.path.pardir, os.path.pardir))
    print('Adding path: ', project_path)
    sys.path.append(project_path)
# Own code
from config import *
import db_management.mysql.check_content as check_mysql
from netgear_code.get_netgear import get_netgear_devices


# Obtaining netgear_code devices
A = get_netgear_devices()

# Create database...
con = pymysql.connect('localhost', MYSQL_USER, os.environ['seb_mysql_key'])
cursor = con.cursor()

print('Creating database: ', DB_NAME_NETGEAR)
cursor.execute("CREATE DATABASE IF NOT EXISTS {0}".format(DB_NAME_NETGEAR))
res = check_mysql.check_database_name(cursor, DB_NAME_NETGEAR)


# Create engine
engine = sqlalchemy.create_engine('mysql+pymysql://{user}:{password}@localhost/{db}'.format(user=MYSQL_USER,
                                                                                    password=os.environ['seb_mysql_key'],
                                                                                    db=DB_NAME_NETGEAR))

# Add data to the database
A.to_sql(DB_NAME_NETGEAR, con=engine, index=False)

# Empty the content of the database - so we are only left with the schema
cursor.execute("USE {db_name}".format(db_name=DB_NAME_NETGEAR))
cursor.execute("TRUNCATE TABLE {table_name}".format(table_name=TABLE_NAME_NETGEAR))
check_mysql.check_table_name(cursor, TABLE_NAME_NETGEAR, DB_NAME_NETGEAR)

# Check content
cursor.execute("SELECT * FROM {table_name};".format(table_name=TABLE_NAME_NETGEAR))
B = cursor.fetchall()

print('Content of table: {table_name}'.format(table_name=TABLE_NAME_NETGEAR))
for x in B:
    print(x)
